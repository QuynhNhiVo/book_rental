from sqlalchemy.orm import Session
from infrastructure.db_models.models import BookModel
from domain.models.book import Book

class BookRepository:
    def __init__(self, db_session:Session):
        self.db = db_session
    
    def get_by_code(self,book_code: str):
        return self.db.query(BookModel).filter(BookModel.BookCode==book_code).first()

    def get_all(self):
        return self.db.query(BookModel).all()
    
    def add_book(self, book: Book):
        new_book = BookModel(
            BookCode = book.book_code,
            Title = book.title,
            Author = book.author,
            Category = book.category,
            Publisher = book.publisher,
            PublishYear = book.publish_year,
            BookStatus = book.book_status
        )
        self.db.add(new_book)
        self.db.commit
        self.db.refresh(new_book)
        return new_book
    
    def delete_book(self, book_code: str) -> bool:
        db_book = self.get_by_code(book_code)
        if not db_book:
            return False
        if db_book.BookStatus == "Rented":
            return False
        self.db.delete(book_code)
        self.db.commit
        return True
    
    def search_books(self, keyword: str):
        search_term = f"%{keyword}%"
        return self.db.query(BookModel).filter(
            (BookModel.Title.ilike(search_term)) |
            (BookModel.Author.ilike(search_term)) |
            (BookModel.Category.ilike(search_term))
        ).all()