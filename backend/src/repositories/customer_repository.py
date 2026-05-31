from ..configs.database import get_connection, execute_query, fetch_one, fetch_query
from ..models.customer import Customer

class CustomerRepository:
    """
    Repository quản lý dữ liệu Khách hàng.
    """
    
    def create(self, customer: Customer) -> int:
        conn = get_connection()
        if not conn: return None
        try:
            query = """
                INSERT INTO Customers (CustomerCode, FullName, Phone, Address, Email)
                VALUES (@customer_code, @full_name, @phone, @address, @email)
            """
            return execute_query(conn, query, {
                'customer_code': customer.customer_code, 
                'full_name': customer.fullname, 
                'phone': customer.phone,
                'address': customer.address, 
                'email': customer.email
            })
        finally:
            conn.close()
    
    def get_by_id(self, customer_id: int) -> Customer:
        conn = get_connection()
        if not conn: return None
        try:
            query = "SELECT * FROM Customers WHERE CustomerID = @customer_id"
            result = fetch_one(conn, query, {'customer_id': customer_id})
            return self._map_to_customer(result) if result else None
        finally:
            conn.close()

    def get_all(self) -> list:
        conn = get_connection()
        if not conn: return []
        try:
            query = "SELECT * FROM Customers ORDER BY CustomerCode"
            results = fetch_query(conn, query)
            return [self._map_to_customer(row) for row in results]
        finally:
            conn.close()

    def update(self, customer: Customer) -> bool:
        conn = get_connection()
        if not conn: return False
        try:
            query = """
                UPDATE Customers 
                SET CustomerCode = @customer_code, FullName = @full_name, 
                    Phone = @phone, Address = @address, Email = @email
                WHERE CustomerID = @customer_id
            """
            result = execute_query(conn, query, {
                'customer_code': customer.customer_code, 'full_name': customer.fullname, 
                'phone': customer.phone, 'address': customer.address, 
                'email': customer.email, 'customer_id': customer.customer_id
            })
            return result is not None
        finally:
            conn.close()

    def delete(self, customer_id: int) -> bool:
        conn = get_connection()
        if not conn: return False
        try:
            query = "DELETE FROM Customers WHERE CustomerID = @customer_id"
            result = execute_query(conn, query, {'customer_id': customer_id})
            return result is not None
        finally:
            conn.close()

    def _map_to_customer(self, row: dict) -> Customer:
        return Customer(
            customer_id=row.get('CustomerID'),
            customer_code=row.get('CustomerCode'),
            fullname=row.get('FullName'),
            phone=row.get('Phone'),
            address=row.get('Address'),
            email=row.get('Email')
        )
