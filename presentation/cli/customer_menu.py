from domain.models.user import User
from datetime import datetime

class CustomerMenu:
    def __init__(self, current_user: User, services: dict):
        self.current_user = current_user
        self.book_service = services.get('book_service')
        self.order_service = services.get('order_service')

    def display(self):
        while True:
            print(f"\n================ MENU CUSTOMER ({self.current_user.username}) ================")
            print("1. Tìm kiếm sách")
            print("2. Xem thông tin sách")
            print("3. Xem trạng thái sách")
            print("4. Chọn thuê sách")
            print("5. Xem sách mình đang thuê")
            print("6. Đăng xuất")
            print("===============================================================")
            
            choice = input("Chọn chức năng: ").strip()

            if choice == '1':
                self._handle_search_books()
            elif choice == '2' or choice == '3':
                # Gom chung hàm xem thông tin và trạng thái vì dữ liệu đi kèm nhau
                self._handle_view_books()
            elif choice == '4':
                self._handle_rent_book()
            elif choice == '5':
                self._handle_view_my_rented_books()
            elif choice == '6':
                print("Đã đăng xuất.")
                break
            else:
                print("❌ Lựa chọn không hợp lệ.")

    def _handle_search_books(self):
        keyword = input("\nNhập từ khóa (Tên/Tác giả/Thể loại): ").strip()
        books = self.book_service.search_books(keyword)
        if not books: 
            print("❌ Không tìm thấy sách phù hợp.")
            return
        print("\n--- KẾT QUẢ TÌM KIẾM ---")
        for b in books: 
            print(f"ID Database: {b.BookID} | Mã: {b.BookCode} | Tên: {b.Title} | Tác giả: {b.Author} | TT: {b.BookStatus}")

    def _handle_view_books(self):
        books = self.book_service.get_all_books()
        if not books: 
            print("Hệ thống hiện chưa có sách.")
            return
        print("\n--- DANH SÁCH SÁCH TRONG THƯ VIỆN ---")
        for b in books: 
            print(f"ID Database: {b.BookID} | Mã: {b.BookCode} | Tên: {b.Title} | Trạng thái: {b.BookStatus}")

    def _handle_rent_book(self):
        """Khách hàng tự tạo đơn thuê [cite: 371]"""
        print("\n--- CHỌN THUÊ SÁCH ---")
        
        # Nếu user này là Customer, chắc chắn phải có customer_id
        if not self.current_user.customer_id:
            print("❌ Lỗi: Tài khoản của bạn chưa được liên kết với hồ sơ khách hàng. Vui lòng liên hệ Admin.")
            return

        try:
            # Nhập danh sách sách
            book_ids_str = input("Nhập danh sách ID Database sách muốn thuê (cách nhau bởi dấu phẩy, VD: 1,3): ")
            book_ids = [int(id.strip()) for id in book_ids_str.split(",") if id.strip()]
            
            # Nhập ngày dự kiến trả
            date_str = input("Nhập ngày dự kiến trả (DD/MM/YYYY): ")
            expected_return_date = datetime.strptime(date_str, "%d/%m/%Y")

            # Tự động lấy ID của chính khách hàng đang đăng nhập
            order_code = self.order_service.create_rental_order(
                customer_id=self.current_user.customer_id, 
                book_ids=book_ids, 
                expected_return_date=expected_return_date
            )
            print(f"✅ Tạo đơn thuê thành công! Mã đơn của bạn là: {order_code}. Vui lòng đến quầy nhận sách.")

        except ValueError as e:
            print(f"❌ Lỗi: {e}")
        except Exception as e:
            print(f"❌ Lỗi hệ thống: {e}")

    def _handle_view_my_rented_books(self):
        """Xem các sách đang thuê của chính khách hàng này [cite: 376]"""
        print("\n--- SÁCH ĐANG THUÊ ---")
        
        if not self.current_user.customer_id:
            print("Tài khoản chưa được liên kết với hồ sơ khách hàng.")
            return
            
        try:
            # Lấy tất cả đơn, sau đó lọc ra những đơn của khách hàng này và đang có trạng thái Renting
            all_orders = self.order_service.get_all_orders()
            my_active_orders = [o for o in all_orders if o.CustomerID == self.current_user.customer_id and o.OrderStatus == 'Renting']
            
            if not my_active_orders:
                print("Bạn hiện không thuê cuốn sách nào.")
                return
                
            for order in my_active_orders:
                print(f"\n[Đơn thuê: {order.OrderCode} - Phải trả trước: {order.ExpectedReturnDate.strftime('%d/%m/%Y')}]")
                for detail in order.details:
                    print(f" - {detail.book.Title} (Mã: {detail.book.BookCode})")
        except Exception as e:
            print(f"❌ Lỗi truy xuất dữ liệu: {e}")