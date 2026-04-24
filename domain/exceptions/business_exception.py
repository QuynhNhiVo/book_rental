# domain/exceptions/business_exception.py

class BusinessException(Exception):
    """Base exception for business logic errors"""
    def __init__(self, message: str, code: str = None):
        self.message = message
        self.code = code
        super().__init__(self.message)

class BookNotFoundError(BusinessException):
    def __init__(self, book_code: str):
        super().__init__(f"Book with code {book_code} not found", "BOOK_NOT_FOUND")

class BookNotAvailableError(BusinessException):
    def __init__(self, book_code: str):
        super().__init__(f"Book {book_code} is not available for rent", "BOOK_NOT_AVAILABLE")

class CustomerNotFoundError(BusinessException):
    def __init__(self, customer_code: str):
        super().__init__(f"Customer with code {customer_code} not found", "CUSTOMER_NOT_FOUND")

class OrderNotFoundError(BusinessException):
    def __init__(self, order_code: str):
        super().__init__(f"Order with code {order_code} not found", "ORDER_NOT_FOUND")

class DuplicateCodeError(BusinessException):
    def __init__(self, entity: str, code: str):
        super().__init__(f"{entity} with code {code} already exists", "DUPLICATE_CODE")

class InvalidStatusTransitionError(BusinessException):
    def __init__(self, from_status: str, to_status: str):
        super().__init__(f"Cannot transition from {from_status} to {to_status}", "INVALID_STATUS")