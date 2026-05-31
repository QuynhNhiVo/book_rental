import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Đường dẫn gốc của dự án
BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent

class Settings:
    """
    Quản lý cấu hình ứng dụng.
    Dữ liệu được lấy từ file .env để đảm bảo bảo mật.
    """
    # Database (SQL Server)
    DB_SERVER = os.getenv("DB_SERVER", "localhost\\SQLEXPRESS")
    DB_NAME = os.getenv("DB_NAME", "BookRentalDB")
    DB_USER = os.getenv("DB_USER", "sa")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "")
    
    # API
    API_HOST = os.getenv("API_HOST", "0.0.0.0")
    API_PORT = int(os.getenv("API_PORT", 5000))
    SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-for-dev-only")

# Khởi tạo instance duy nhất (Singleton)
settings = Settings()
