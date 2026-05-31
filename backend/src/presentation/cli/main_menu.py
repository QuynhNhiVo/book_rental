"""Main Menu - Login and role selection"""
from domain.models import User
from domain.exceptions.business_exception import AuthenticationError, UnauthorizedError
from presentation.cli.admin_menu import AdminMenu
from presentation.cli.customer_menu import CustomerMenu

class MainMenu:
    """Main menu for authentication and navigation"""
    
    def __init__(self, auth_service, services_dict):
        self.auth_service = auth_service
        self.services_dict = services_dict
        self.current_user = None
    
    def display(self):
        """Display main menu loop"""
        while True:
            print("\n" + "="*45)
            print("📌 MENU CHÍNH - HỆ THỐNG QUẢN LÝ THUÊ SÁCH")
            print("="*45)
            print("1. 🔐 Đăng nhập")
            print("2. 🚪 Thoát")
            print("="*45)

            choice = input("Chọn chức năng (1-2): ").strip()

            if choice == "1":
                self.login()
            elif choice == "2":
                self.exit_app()
            else:
                print("❌ Lựa chọn không hợp lệ. Vui lòng thử lại.")

    def login(self):
        """Authenticate user"""
        print("\n" + "-"*45)
        print("🔐 ĐĂNG NHẬP")
        print("-"*45)

        username = input("Tên đăng nhập: ").strip()
        password = input("Mật khẩu: ").strip()

        try:
            user = self.auth_service.login(username, password)
            self.current_user = user
            print(f"\n✅ Đăng nhập thành công! Chào mừng {username}")

            # Route to appropriate menu based on role
            if user.role == "Admin":
                admin_menu = AdminMenu(user, self.services_dict)
                admin_menu.display()
            elif user.role == "Customer":
                customer_menu = CustomerMenu(user, self.services_dict)
                customer_menu.display()
            else:
                print(f"❌ Vai trò không xác định: {user.role}")

        except AuthenticationError as e:
            print(f"❌ {e.message}")
        except UnauthorizedError as e:
            print(f"❌ {e.message}")
        except Exception as e:
            print(f"❌ Lỗi trong quá trình đăng nhập: {e}")

    def exit_app(self):
        """Exit application"""
        print("\n" + "="*45)
        print("👋 Cảm ơn bạn đã sử dụng Hệ thống Quản lý Thuê Sách!")
        print("Tạm biệt!\n")
        print("="*45)
        exit(0)