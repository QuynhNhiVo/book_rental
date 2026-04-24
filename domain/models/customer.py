from dataclasses import dataclass
from typing import Optional

from domain.exceptions.business_exception import BusinessException


@dataclass
class Customer:
    customer_code: str
    fullname: str
    customer_id: Optional[int] = None
    phone: Optional[int] = None
    address: Optional[str] = None
    email: Optional[str] = None

    def __post_init__(self):
        if not self.customer_code or not self.customer_code.strip():
            raise BusinessException("Customer code is required.")
        if not self.fullname or not self.fullname.strip():
            raise BusinessException("Customer fullname is required.")
        if self.email is not None and not self.email.strip():
            raise BusinessException("Customer email cannot be blank.")
