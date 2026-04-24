class AuthService:
    def __init__(self, user_repository):
        self.user_repo = user_repository

    def login(self, username, password):
        """Xử lý đăng nhập.
            Kiểm tra tài khoản có tồn tại và đúng mật khẩu hay không.
        """
        user = self.user_repo.authenticate(username, password)
        if not user:
            raise ValueError("Đăng nhập thất bại: Sai tên đăng nhập hoặc mật khẩu.")
        
        # Trả về đối tượng Domain User chứa thông tin Role và CustomerID
        return user