from datetime import datetime
from ..configs.database import get_connection, execute_query, fetch_one, fetch_query
from ..models.order import RentalOrder

class OrderRepository:
    """
    Repository quản lý dữ liệu Đơn thuê sách.
    """
    
    def create_order(self, order: RentalOrder, book_ids: list) -> int:
        conn = get_connection()
        if not conn: return None
        cursor = None
        try:
            cursor = conn.cursor()
            # 1. Tạo đơn thuê
            query = """
                INSERT INTO RentalOrders (OrderCode, CustomerID, RentDate, ExpectedReturnDate, OrderStatus)
                VALUES (@order_code, @customer_id, @rent_date, @expected_return_date, @order_status)
            """
            cursor.execute(query, {
                'order_code': order.order_code, 'customer_id': order.customer_id, 
                'rent_date': order.rent_date, 'expected_return_date': order.expected_return_date, 
                'order_status': order.order_status
            })
            
            # Lấy ID vừa tạo
            cursor.execute("SELECT SCOPE_IDENTITY() as OrderID")
            row = cursor.fetchone()
            order_id = row.get('OrderID') if row else None
            
            # 2. Tạo chi tiết và cập nhật trạng thái sách
            for book_id in book_ids:
                cursor.execute("INSERT INTO RentalOrderDetails (OrderID, BookID) VALUES (@oid, @bid)", 
                              {'oid': order_id, 'bid': book_id})
                cursor.execute("UPDATE Books SET BookStatus = 'Rented' WHERE BookID = @bid", 
                              {'bid': book_id})
            
            conn.commit()
            return order_id
        except Exception as e:
            conn.rollback()
            print(f"❌ Lỗi tạo đơn: {e}")
            return None
        finally:
            if cursor: cursor.close()
            conn.close()

    def process_return(self, order_id: int) -> bool:
        conn = get_connection()
        if not conn: return False
        cursor = None
        try:
            cursor = conn.cursor()
            # 1. Lấy danh sách sách trong đơn
            cursor.execute("SELECT BookID FROM RentalOrderDetails WHERE OrderID = @oid", {'oid': order_id})
            books = cursor.fetchall()
            
            # 2. Cập nhật trạng thái đơn
            cursor.execute("""
                UPDATE RentalOrders SET ReturnDate = @now, OrderStatus = 'Returned'
                WHERE OrderID = @oid AND OrderStatus = 'Renting'
            """, {'now': datetime.now(), 'oid': order_id})
            
            # 3. Cập nhật trạng thái sách
            for b in books:
                bid = b.get('BookID')
                cursor.execute("UPDATE Books SET BookStatus = 'Available' WHERE BookID = @bid", {'bid': bid})
            
            conn.commit()
            return True
        except Exception as e:
            conn.rollback()
            print(f"❌ Lỗi trả sách: {e}")
            return False
        finally:
            if cursor: cursor.close()
            conn.close()

    def get_all(self) -> list:
        conn = get_connection()
        if not conn: return []
        try:
            query = "SELECT * FROM RentalOrders ORDER BY RentDate DESC"
            results = fetch_query(conn, query)
            return [self._map_to_order(row) for row in results]
        finally:
            conn.close()

    def get_customer_orders(self, customer_id: int) -> list:
        conn = get_connection()
        if not conn: return []
        try:
            query = "SELECT * FROM RentalOrders WHERE CustomerID = @cid ORDER BY RentDate DESC"
            results = fetch_query(conn, query, {'cid': customer_id})
            return [self._map_to_order(row) for row in results]
        finally:
            conn.close()

    def _map_to_order(self, row: dict) -> RentalOrder:
        return RentalOrder(
            order_id=row.get('OrderID'),
            order_code=row.get('OrderCode'),
            customer_id=row.get('CustomerID'),
            rent_date=row.get('RentDate'),
            expected_return_date=row.get('ExpectedReturnDate'),
            return_date=row.get('ReturnDate'),
            order_status=row.get('OrderStatus')
        )
