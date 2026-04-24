import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

class Settings:

    # Lấy thông tin kết nối, nếu không có trong .env thì dùng giá trị mặc định
    DB_SERVER = os.getenv("DB_SERVER", r"localhost\SQLEXPRESS")
    DB_NAME = os.getenv("DB_NAME", "BookRentalDB")
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")

    # Chuỗi kết nối dành riêng cho SQL Server thông qua pyodbc
    DATABASE_URL = (
        f"mssql+pyodbc://{DB_USER}:{DB_PASSWORD}@{DB_SERVER}/{DB_NAME}"
        f"?driver=ODBC+Driver+17+for+SQL+Server"
    )
    # Logging
    LOG_FILE = BASE_DIR / "logs" / "app.log"
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

settings = Settings()

