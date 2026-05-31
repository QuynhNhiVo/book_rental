from dataclasses import dataclass
from typing import Optional
from datetime import datetime
from ..utils.exceptions import BusinessException

@dataclass
class Customer:
    """
    Model đại diện cho Khách hàng.
    """
    customer_code: str
    fullname: str
    customer_id: Optional[int] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    email: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def __post_init__(self):
        if not self.customer_code or not self.customer_code.strip():
            raise BusinessException("Mã khách hàng là bắt buộc.")
        if not self.fullname or not self.fullname.strip():
            raise BusinessException("Họ tên khách hàng là bắt buộc.")
