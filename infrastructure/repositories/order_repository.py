from sqlalchemy.orm import Session
from datetime import datetime
from infrastructure.db_models.models import RentalOrderModel, RentalOrderDetailModel, BookModel
from domain.models.order import RentalOrder

class OrderRepository:
    def __init__(self, db_session: Session):
        self.db = db_session

    def create_order(self, order: RentalOrder, book_ids: list[int]) -> str | None:
        """Tạo đơn thuê mới và cập nhật trạng thái sách (Dùng Transaction)"""
        try:
            # 1. Tạo record cho đơn thuê
            db_order = RentalOrderModel(
                OrderCode=order.order_code,
                CustomerID=order.customer_id,
                RentDate=order.rent_date,
                ExpectedReturnDate=order.expected_return_date,
                OrderStatus=order.order_status
            )
            self.db.add(db_order)
            self.db.flush() # Đẩy xuống DB để lấy ID, nhưng chưa commit

            # 2. Thêm chi tiết đơn và cập nhật trạng thái sách
            for book_id in book_ids:
                # Thêm chi tiết
                db_detail = RentalOrderDetailModel(OrderID=db_order.OrderID, BookID=book_id)
                self.db.add(db_detail)
                
                # Cập nhật sách sang 'Rented'
                db_book = self.db.query(BookModel).filter(BookModel.BookID == book_id).first()
                if db_book:
                    db_book.BookStatus = 'Rented'

            # 3. Mọi thứ OK -> Xác nhận lưu
            self.db.commit()
            return db_order.OrderCode
            
        except Exception as e:
            self.db.rollback() # Có lỗi -> Hoàn tác mọi thay đổi
            print(f"Lỗi khi tạo đơn: {e}")
            return None

    def process_return(self, order_code: str) -> bool:
        """Ghi nhận trả sách: Cập nhật đơn và chuyển sách về Available"""
        try:
            db_order = self.db.query(RentalOrderModel).filter(RentalOrderModel.OrderCode == order_code).first()
            if not db_order or db_order.OrderStatus != 'Renting':
                return False

            # Cập nhật đơn
            db_order.ReturnDate = datetime.now()
            db_order.OrderStatus = 'Returned'

            # Cập nhật trạng thái tất cả sách trong đơn về 'Available'
            for detail in db_order.details:
                detail.book.BookStatus = 'Available'

            self.db.commit()
            return True
            
        except Exception as e:
            self.db.rollback()
            return False
        
    def get_all(self):
        return self.db.query(RentalOrderModel).all()

    def get_by_code(self, order_code: str):
        return self.db.query(RentalOrderModel).filter(RentalOrderModel.OrderCode == order_code).first()

    def get_renting_books_by_customer(self, customer_id: int):
        """Dùng cho chức năng khách hàng xem sách đang thuê"""
        return self.db.query(RentalOrderModel).filter(
            RentalOrderModel.CustomerID == customer_id,
            RentalOrderModel.OrderStatus == 'Renting'
        ).all()