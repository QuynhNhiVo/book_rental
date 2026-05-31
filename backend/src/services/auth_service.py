from ..utils.exceptions import AuthenticationError
from ..models.user import User

class AuthService:
    """
    Service xử lý các nghiệp vụ liên quan đến xác thực người dùng.
    """
    
    def __init__(self, user_repository):
        self.user_repo = user_repository
    
    def login(self, username: str, password: str) -> User:
        """
        Xử lý đăng nhập.
        1. Kiểm tra username/password có trống không.
        2. Xác thực mật khẩu thông qua repository.
        3. Trả về thông tin User nếu thành công.
        """
        if not username or not password:
            raise AuthenticationError("Vui lòng nhập đầy đủ tên đăng nhập và mật khẩu.")
        
        if not self.user_repo.verify_password(username, password):
            raise AuthenticationError("Tên đăng nhập hoặc mật khẩu không chính xác.")
        
        user = self.user_repo.get_by_username(username)
        if not user:
            raise AuthenticationError("Người dùng không tồn tại.")
        
        return user
