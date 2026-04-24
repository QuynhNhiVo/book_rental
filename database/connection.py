from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config.settings import settings
from infrastructure.db_models.base import Base

from infrastructure.db_models import models
# Tạo Engine
engine = create_engine(
    settings.DATABASE_URL,
    echo=False,
    fast_executemany=True # Tính năng tối ưu hóa tốc độ Insert cho SQL Server / pyodbc
)

# Tạo Session Factory
# autocommit=False: Bắt buộc phải gọi db.commit() thì dữ liệu mới lưu (Bảo vệ tính toàn vẹn)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
def init_db():
    """Hàm khởi tạo: Tự động quét các model và tạo bảng trong SQL Server nếu chưa có"""
    try:
        Base.metadata.create_all(bind=engine)
        print("Khởi tạo cấu trúc Database thành công!")
    except Exception as e:
        print(f"Lỗi khi khởi tạo Database: {e}")

def get_db():
    """
    Hàm cung cấp Session. Sử dụng 'yield' (Generator) để đảm bảo 
    luôn tự động đóng kết nối (db.close()) sau khi xử lý xong, chống tràn bộ nhớ.
    """
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()