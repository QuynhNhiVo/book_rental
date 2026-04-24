from dataclasses import dataclass
from typing import Optional
from exceptions.business_exception import BusinessException

@dataclass
class Book:
    book_code: str
    title: str
    author: str
    book_id: Optional[int] = None
    book_status: str = 'Available'  # 'Available' hoặc 'Rented'
    category: Optional[str] = None
    publisher: Optional[str] = None
    publish_year: Optional[int] = None

    def is_available(self) -> bool:
        return self.book_status == 'Available'
        
    def mark_as_rented(self):
        if not self.is_available():
            raise BusinessException(f"Book {self.book_code} is not available")
        self.book_status = 'Rented'
        
    def mark_as_available(self):
        self.book_status = 'Available'

    def to_dict(self):
        return {
            'book_id': self.book_id,
            'book_code': self.book_code,
            'title': self.title,
            'author': self.author,
            'category': self.category,
            'publisher': self.publisher,
            'publish_year': self.publish_year,
            'status': self.status.value
        }