from ..models.book import Book
from ..utils.exceptions import BookNotFoundError, BusinessException

class BookService:
    """
    Service quản lý các nghiệp vụ liên quan đến Sách.
    """
    
    def __init__(self, book_repository):
        self.book_repo = book_repository
    
    def create_book(self, book: Book) -> int:
        return self.book_repo.create(book)
    
    def get_all_books(self) -> list:
        return self.book_repo.get_all()
    
    def get_book_by_id(self, book_id: int) -> Book:
        book = self.book_repo.get_by_id(book_id)
        if not book:
            raise BookNotFoundError(book_id=book_id)
        return book
    
    def update_book(self, book: Book) -> bool:
        if not self.book_repo.get_by_id(book.book_id):
            raise BookNotFoundError(book_id=book.book_id)
        return self.book_repo.update(book)
    
    def delete_book(self, book_id: int) -> bool:
        book = self.get_book_by_id(book_id)
        if book.book_status != 'Available':
            raise BusinessException("Chỉ có thể xóa sách đang ở trạng thái 'Available'.")
        return self.book_repo.delete(book_id)
