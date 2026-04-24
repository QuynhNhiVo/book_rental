from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional

from domain.exceptions.business_exception import BusinessException


@dataclass
class RentalOrderDetail:
    book_id: int
    order_id: Optional[int] = None
    order_detail_id: Optional[int] = None


@dataclass
class RentalOrder:
    order_code: str
    customer_id: int
    rent_date: datetime
    expected_return_date: datetime
    order_id: Optional[int] = None
    order_status: str = "Renting"
    return_date: Optional[datetime] = None
    details: List[RentalOrderDetail] = field(default_factory=list)

    def __post_init__(self):
        if not self.order_code or not self.order_code.strip():
            raise BusinessException("Order code is required.")
        if self.customer_id <= 0:
            raise BusinessException("Customer id must be greater than 0.")
        if self.order_status not in {"Renting", "Returned"}:
            raise BusinessException("Order status must be Renting or Returned.")
        if self.expected_return_date < self.rent_date:
            raise BusinessException("Expected return date must be after rent date.")
        if self.return_date is not None and self.return_date < self.rent_date:
            raise BusinessException("Return date cannot be before rent date.")

    def is_active(self) -> bool:
        return self.order_status == "Renting"

    def add_book(self, book_id: int):
        if book_id <= 0:
            raise BusinessException("Book id must be greater than 0.")
        if any(detail.book_id == book_id for detail in self.details):
            raise BusinessException("Book already exists in this order.")
        detail = RentalOrderDetail(book_id=book_id)
        self.details.append(detail)

    def process_return(self, return_date: datetime):
        if not self.is_active():
            raise BusinessException("Order has already been returned.")
        if return_date < self.rent_date:
            raise BusinessException("Return date cannot be before rent date.")
        self.return_date = return_date
        self.order_status = "Returned"
