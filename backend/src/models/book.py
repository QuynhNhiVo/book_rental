from dataclasses import dataclass
from typing import Optional
from datetime import datetime
from ..utils.exceptions import BusinessException

@dataclass
class Book:
    """
    Model đại diện cho Sách.
    """
    book_code: str
    title: str
    author: str
    book_id: Optional[int] = None
    book_status: str = 'Available'
    category: Optional[str] = None
    publisher: Optional[str] = None
    publish_year: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def is_available(self) -> bool:
        return self.book_status == 'Available'

    def to_dict(self) -> dict:
        return {
            'book_id': self.book_id,
            'book_code': self.book_code,
            'title': self.title,
            'author': self.author,
            'category': self.category,
            'publisher': self.publisher,
            'publish_year': self.publish_year,
            'book_status': self.book_status
        }
