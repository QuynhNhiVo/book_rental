from datetime import datetime
from ..models.order import RentalOrder
from ..utils.exceptions import BookNotFoundError, CustomerNotFoundError, OrderNotFoundError, BusinessException

class OrderService:
    """
    Service quản lý các nghiệp vụ liên quan đến Đơn thuê.
    """
    
    def __init__(self, order_repository, book_repository, customer_repository):
        self.order_repo = order_repository
        self.book_repo = book_repository
        self.customer_repo = customer_repository

    def create_order(self, order: RentalOrder, book_ids: list) -> int:
        """Tạo đơn thuê sách mới với các ràng buộc nghiệp vụ."""
        if not self.customer_repo.get_by_id(order.customer_id):
            raise CustomerNotFoundError(customer_id=order.customer_id)

        if not book_ids:
            raise BusinessException("Đơn thuê phải có ít nhất một cuốn sách.")

        for book_id in book_ids:
            book = self.book_repo.get_by_id(book_id)
            if not book:
                raise BookNotFoundError(book_id=book_id)
            if book.book_status != 'Available':
                raise BusinessException(f"Sách '{book.title}' hiện không sẵn sàng để thuê.")

        return self.order_repo.create_order(order, book_ids)

    def process_return(self, order_id: int) -> bool:
        """Xử lý trả sách."""
        order = self.order_repo.get_by_id(order_id)
        if not order:
            raise OrderNotFoundError(order_id=order_id)
        if order.order_status != 'Renting':
            raise BusinessException("Đơn hàng này đã được trả hoặc không ở trạng thái đang thuê.")
        
        return self.order_repo.process_return(order_id)

    def get_all_orders(self) -> list:
        return self.order_repo.get_all()

    def get_customer_orders(self, customer_id: int) -> list:
        return self.order_repo.get_customer_orders(customer_id)
    
    def get_customer_renting_orders(self, customer_id: int) -> list:
        all_orders = self.get_customer_orders(customer_id)
        return [o for o in all_orders if o.order_status == 'Renting']
