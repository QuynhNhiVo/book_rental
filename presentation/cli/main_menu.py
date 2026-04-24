from application.services.auth_service import AuthService
from presentation.cli.admin_menu import AdminMenu
from presentation.cli.customer_menu import CustomerMenu

class MainMenu:
    def __init__(self, auth_service: AuthService, services_dict: dict):
        self.auth_service = auth_service
        self.services = services_dict

    def display(self):
        while True:
            print("\n================ BOOK RENTAL STORE ================")
            print("1. Đăng nhập Admin")
            print("2. Đăng nhập Customer")
            print("3. Thoát")
            print("===================================================")
            
            choice = input("Chọn chức năng: ").strip()

            if choice == '1':
                self._handle_login(role='Admin')
            elif choice == '2':
                self._handle_login(role='Customer')
            elif choice == '3':
                print("Cảm ơn bạn đã sử dụng hệ thống. Tạm biệt!")
                break
            else:
                print("❌ Lựa chọn không hợp lệ. Vui lòng chọn lại.")

    def _handle_login(self, role: str):
        print(f"\n--- ĐĂNG NHẬP {role.upper()} ---")
        username = input("Username: ").strip()
        password = input("Password: ").strip()

        try:
            user = self.auth_service.login(username, password)
            
            if user.role != role:
                print(f"❌ Lỗi: Tài khoản này không có quyền {role}.")
                return

            print(f"✅ Đăng nhập thành công! Xin chào, {user.username}.")
            
            # Điều hướng sang menu tương ứng
            if role == 'Admin':
                AdminMenu(self.services).display()
            else:
                CustomerMenu(user, self.services).display()

        except ValueError as e:
            print(f"❌ {e}")