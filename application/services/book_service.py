from domain.models.book import Book

class BookService:
    def __init__(self, book_repository):
        self.book_repo = book_repository

    def add_book(self, book: Book):
        """Thêm sách mới"""
        # Quy tắc: Kiểm tra mã sách có bị trùng không
        existing_book = self.book_repo.get_by_code(book.book_code)
        if existing_book:
            raise ValueError(f"Lỗi: Mã sách '{book.book_code}' đã tồn tại.")
        
        return self.book_repo.add_book(book)

    def get_all_books(self):
        """Xem danh sách sách"""
        return self.book_repo.get_all()

    def search_books(self, keyword: str):
        """Tìm kiếm sách theo tên, tác giả, thể loại"""
        return self.book_repo.search_books(keyword)

    def delete_book(self, book_code: str):
        """Xóa sách"""
        book = self.book_repo.get_by_code(book_code)
        if not book:
            raise ValueError("Không tìm thấy sách.")
            
        # Quy tắc: Không cho xóa sách nếu sách đang được thuê
        if book.BookStatus == 'Rented':
            raise ValueError("Từ chối xóa: Sách đang được thuê")
            
        return self.book_repo.delete_book(book_code)

    def update_book_status(self, book_code: str, new_status: str):
        """Cập nhật trạng thái sách thủ công"""
        if new_status not in ['Available', 'Rented']:
            raise ValueError("Trạng thái chỉ được là 'Available' hoặc 'Rented'.")
            
        book = self.book_repo.get_by_code(book_code)
        if not book:
            raise ValueError("Không tìm thấy sách.")
            
        return self.book_repo.update_status(book_code, new_status)