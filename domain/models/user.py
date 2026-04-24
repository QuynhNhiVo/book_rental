from dataclasses import dataclass
from typing import Optional

from domain.exceptions.business_exception import BusinessException


@dataclass
class User:
    username: str
    password: str
    role: str
    user_id: Optional[int] = None
    customer_id: Optional[int] = None

    def __post_init__(self):
        if not self.username or not self.username.strip():
            raise BusinessException("Username is required.")
        if not self.password or not self.password.strip():
            raise BusinessException("Password is required.")
        if self.role not in {"Admin", "Customer"}:
            raise BusinessException("Role must be Admin or Customer.")
        self.validate_role()

    def is_admin(self) -> bool:
        return self.role == "Admin"

    def validate_role(self) -> bool:
        if self.role == "Admin" and self.customer_id is not None:
            raise BusinessException("Admin user must not have customer_id.")
        if self.role == "Customer" and self.customer_id is None:
            raise BusinessException("Customer user must have customer_id.")
        return True
