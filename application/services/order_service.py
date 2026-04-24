from datetime import datetime
from domain.models.order import RentalOrder

class OrderService:
    def __init__(self, order_repository, book_repository, customer_repository):
        self.order_repo = order_repository
        self.book_repo = book_repository
        self.customer_repo = customer_repository

    def create_rental_order(self, customer_id: int, book_ids: list[int], expected_return_date: datetime):
        """Tạo đơn thuê cho Admin [cite: 177] và Customer [cite: 193]"""
        
        # 1. Kiểm tra khách hàng tồn tại [cite: 178]
        if not self.customer_repo.get_by_id(customer_id):
            raise ValueError("Khách hàng không tồn tại.")

        # 2. Kiểm tra danh sách sách [cite: 178]
        if not book_ids:
            raise ValueError("Đơn thuê phải chứa ít nhất một cuốn sách.")

        for book_id in book_ids:
            book = self.book_repo.get_by_id(book_id)
            if not book:
                raise ValueError(f"Sách có ID {book_id} không tồn tại.")
            # Quy tắc: Chỉ sách ở trạng thái Available mới được thuê [cite: 201]
            if book.BookStatus != 'Available':
                raise ValueError(f"Sách '{book.Title}' đang không có sẵn để thuê[cite: 194].")

        # 3. Kiểm tra ngày trả dự kiến [cite: 232]
        rent_date = datetime.now()
        if expected_return_date < rent_date:
            raise ValueError("Ngày dự kiến trả sách phải lớn hơn hoặc bằng ngày thuê[cite: 232].")

        # 4. Khởi tạo Domain Model
        order_code = f"ORD{int(datetime.now().timestamp())}"
        new_order = RentalOrder(
            order_code=order_code,
            customer_id=customer_id,
            rent_date=rent_date,
            expected_return_date=expected_return_date,
            order_status='Renting'
        )

        # 5. Gửi xuống Repository để xử lý Transaction lưu Database
        result = self.order_repo.create_order(new_order, book_ids)
        if not result:
            raise Exception("Đã xảy ra lỗi hệ thống khi lưu đơn thuê.")
        return result

    def process_return(self, order_code: str):
        """Ghi nhận trả sách [cite: 181]"""
        # Việc kiểm tra đơn tồn tại và cập nhật trạng thái đơn/sách 
        # đã được bao bọc an toàn trong Transaction của OrderRepository.
        success = self.order_repo.process_return(order_code)
        if not success:
            raise ValueError("Không thể ghi nhận trả sách. Vui lòng kiểm tra lại mã đơn[cite: 182].")
        return True
        
    def get_customer_renting_books(self, customer_id: int):
        """Lấy danh sách sách đang thuê của một Customer (Dùng cho Menu Customer B5) [cite: 195]"""
        return self.order_repo.get_renting_books_by_customer(customer_id)