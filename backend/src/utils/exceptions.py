class BusinessException(Exception):
    """Base exception cho các lỗi nghiệp vụ."""
    def __init__(self, message: str, code: str = None):
        self.message = message
        self.code = code
        super().__init__(self.message)

class AuthenticationError(BusinessException):
    def __init__(self, message: str = "Đăng nhập thất bại"):
        super().__init__(message, "AUTH_FAILED")

class UnauthorizedError(BusinessException):
    def __init__(self, message: str = "Không có quyền truy cập"):
        super().__init__(message, "UNAUTHORIZED")

class BookNotFoundError(BusinessException):
    def __init__(self, book_id: int = None):
        super().__init__(f"Không tìm thấy sách với ID {book_id}", "BOOK_NOT_FOUND")

class CustomerNotFoundError(BusinessException):
    def __init__(self, customer_id: int = None):
        super().__init__(f"Không tìm thấy khách hàng với ID {customer_id}", "CUSTOMER_NOT_FOUND")

class OrderNotFoundError(BusinessException):
    def __init__(self, order_id: int = None):
        super().__init__(f"Không tìm thấy đơn hàng với ID {order_id}", "ORDER_NOT_FOUND")

class InvalidDateError(BusinessException):
    def __init__(self, message: str = "Ngày trả dự kiến phải sau ngày thuê"):
        super().__init__(message, "INVALID_DATE")
