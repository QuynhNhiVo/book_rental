from werkzeug.security import generate_password_hash, check_password_hash
from ..configs.database import get_connection, execute_query, fetch_one, fetch_query
from ..models.user import User

class UserRepository:
    """
    Repository quản lý các thao tác Database liên quan đến User.
    """
    
    def create(self, user: User) -> int:
        conn = get_connection()
        if not conn: return None
        hashed_password = generate_password_hash(user.password)
        try:
            query = """
                INSERT INTO Users (Username, Password, Role, CustomerID)
                VALUES (@username, @password, @role, @customer_id)
            """
            return execute_query(conn, query, {
                'username': user.username, 
                'password': hashed_password, 
                'role': user.role, 
                'customer_id': user.customer_id
            })
        finally:
            conn.close()
    
    def get_by_username(self, username: str) -> User:
        conn = get_connection()
        if not conn: return None
        try:
            query = "SELECT UserID, Username, Password, Role, CustomerID FROM Users WHERE Username = @username"
            result = fetch_one(conn, query, {'username': username})
            return self._map_to_user(result) if result else None
        finally:
            conn.close()
    
    def verify_password(self, username: str, password: str) -> bool:
        user = self.get_by_username(username)
        if not user: return False
        return check_password_hash(user.password, password)
    
    def _map_to_user(self, row: dict) -> User:
        return User(
            user_id=row.get('UserID'),
            username=row.get('Username'),
            password=row.get('Password'),
            role=row.get('Role'),
            customer_id=row.get('CustomerID')
        )
