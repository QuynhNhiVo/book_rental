from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional
from ..utils.exceptions import BusinessException

@dataclass
class RentalOrderDetail:
    """Chi tiết từng cuốn sách trong một đơn thuê."""
    book_id: int
    order_id: Optional[int] = None
    order_detail_id: Optional[int] = None

@dataclass
class RentalOrder:
    """Model đại diện cho Đơn thuê sách."""
    order_code: str
    customer_id: int
    rent_date: datetime
    expected_return_date: datetime
    order_id: Optional[int] = None
    order_status: str = "Renting"
    return_date: Optional[datetime] = None
    details: List[RentalOrderDetail] = field(default_factory=list)
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def __post_init__(self):
        if not self.order_code:
            raise BusinessException("Mã đơn hàng là bắt buộc.")
        if self.expected_return_date < self.rent_date:
            raise BusinessException("Ngày trả dự kiến phải sau ngày thuê.")
