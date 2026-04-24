from datetime import datetime
from domain.models.order import RentalOrder

class OrderService:
    def __init__(self, order_repository, book_repository, customer_repository):
        self.order_repo = order_repository
        self.book_repo = book_repository
        self.customer_repo = customer_repository

    def create_rental_order(self, customer_id: int, book_codes: list[str], expected_return_date: datetime):
        """Tạo đơn thuê cho Admin và Customer thông qua MÃ SÁCH"""
        
        # 1. Kiểm tra khách hàng tồn tại
        if not self.customer_repo.get_by_id(customer_id):
            raise ValueError("Khách hàng không tồn tại.")

        # 2. Kiểm tra danh sách sách bằng MÃ SÁCH
        if not book_codes:
            raise ValueError("Đơn thuê phải chứa ít nhất một cuốn sách.")

        book_ids = []
        for code in book_codes:
            book = self.book_repo.get_by_code(code)
            if not book:
                raise ValueError(f"Sách có mã '{code}' không tồn tại trong hệ thống.")
            
            # Quy tắc: Chỉ sách ở trạng thái Available mới được thuê
            if book.BookStatus != 'Available':
                raise ValueError(f"Sách '{book.Title}' (Mã: {code}) đang không có sẵn để thuê.")
            
            # Lưu lại ID Database để truyền xuống tầng Repository
            book_ids.append(book.BookID)

        # 3. Kiểm tra ngày trả dự kiến
        rent_date = datetime.now()
        if expected_return_date < rent_date:
            raise ValueError("Ngày dự kiến trả sách phải lớn hơn hoặc bằng ngày thuê.")

        # 4. Khởi tạo Domain Model
        order_code = f"ORD{int(datetime.now().timestamp())}"
        
        # Lưu ý: Nhớ đảm bảo bạn đã có dòng "from domain.models.order import RentalOrder" ở đầu file
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
            raise ValueError("Không thể ghi nhận trả sách. Vui lòng kiểm tra lại mã đơn")
        return True
        
    def get_customer_renting_books(self, customer_id: int):
        """Lấy danh sách sách đang thuê của một Customer (Dùng cho Menu Customer B5) """
        return self.order_repo.get_renting_books_by_customer(customer_id)

    def get_all_orders(self):
        """Lấy tất cả đơn thuê (Cho Admin)"""
        return self.order_repo.get_all()

    def get_order_by_code(self, order_code: str):
        """Lấy chi tiết 1 đơn thuê"""
        return self.order_repo.get_by_code(order_code)