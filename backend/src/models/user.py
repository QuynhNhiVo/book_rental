from dataclasses import dataclass
from typing import Optional
from datetime import datetime
from ..utils.exceptions import BusinessException

@dataclass
class User:
    """
    Model đại diện cho người dùng hệ thống.
    Sử dụng dataclass để tự động khởi tạo các trường.
    """
    username: str
    password: str
    role: str
    user_id: Optional[int] = None
    customer_id: Optional[int] = None
    created_at: Optional[datetime] = None

    def __post_init__(self):
        # Kiểm tra tính hợp lệ của dữ liệu ngay khi khởi tạo
        if not self.username:
            raise BusinessException("Tên đăng nhập không được để trống.")
        if not self.password:
            raise BusinessException("Mật khẩu không được để trống.")
        if self.role not in {"Admin", "Customer"}:
            raise BusinessException("Vai trò không hợp lệ.")

    def is_admin(self) -> bool:
        return self.role == "Admin"
