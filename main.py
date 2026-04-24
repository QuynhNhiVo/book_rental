from database.connection import init_db, SessionLocal
from infrastructure.repositories.user_repository import UserRepository
from infrastructure.repositories.book_repository import BookRepository
from infrastructure.repositories.order_repository import OrderRepository
from infrastructure.repositories.customer_repository import CustomerRepository

from application.services.auth_service import AuthService
from application.services.book_service import BookService
from application.services.order_service import OrderService
from application.services.customer_service import CustomerService
from application.services.report_service import ReportService

from presentation.cli.main_menu import MainMenu
from infrastructure.db_models.models import UserModel

def seed_admin_account(db_session):
    """Tự động tạo tài khoản Admin mặc định nếu DB chưa có"""
    admin_exists = db_session.query(UserModel).filter(UserModel.Username == "admin").first()
    if not admin_exists:
        default_admin = UserModel(Username="admin", Password="123", Role="Admin")
        db_session.add(default_admin)
        db_session.commit()
        print("✅ Đã tự động tạo tài khoản Admin mặc định (Username: admin | Password: 123)")

def main():
    print("Đang khởi động hệ thống Book Rental...")
    
    # 1. Khởi tạo Database
    init_db()

    # 2. Khởi tạo Session
    db_session = SessionLocal()

    try:
        # Tự động chèn dữ liệu mẫu (Seeding)
        seed_admin_account(db_session)

        # 3. Khởi tạo Repositories (Tầng Infrastructure)
        user_repo = UserRepository(db_session)
        book_repo = BookRepository(db_session)
        order_repo = OrderRepository(db_session)
        customer_repo = CustomerRepository(db_session)
        
        # 4. Khởi tạo Services (Tầng Application)
        auth_service = AuthService(user_repo)
        book_service = BookService(book_repo)
        order_service = OrderService(order_repo, book_repo, customer_repo) 
        customer_service = CustomerService(customer_repo, order_repo)
        report_service = ReportService(book_repo, order_repo)
        
        # Đóng gói TẤT CẢ các service để truyền vào CLI
        services_dict = {
            'book_service': book_service,
            'order_service': order_service,
            'customer_service': customer_service,
            'report_service': report_service
        }

        # 5. Khởi động Giao diện dòng lệnh (Tầng Presentation)
        app_cli = MainMenu(auth_service, services_dict)
        app_cli.display()

    except Exception as e:
        print(f"❌ Lỗi hệ thống nghiêm trọng: {e}")
    finally:
        # Luôn đảm bảo đóng kết nối DB khi thoát phần mềm
        db_session.close()

if __name__ == "__main__":
    main()