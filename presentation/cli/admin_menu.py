from domain.models.book import Book
from domain.models.customer import Customer
from datetime import datetime

class AdminMenu:
    def __init__(self, services: dict):
        self.book_service = services.get('book_service')
        self.order_service = services.get('order_service')
        self.customer_service = services.get('customer_service')
        self.report_service = services.get('report_service')

    def display(self):
        while True:
            print("\n=================== MENU ADMIN ===================")
            print("1. Quản lý sách")
            print("2. Quản lý trạng thái sách")
            print("3. Quản lý khách hàng")
            print("4. Quản lý đơn thuê")
            print("5. Báo cáo")
            print("6. Đăng xuất")
            print("==================================================")
            
            choice = input("Chọn chức năng: ").strip()

            if choice == '1':
                self._manage_books_menu()
            elif choice == '2':
                self._manage_book_status_menu()
            elif choice == '3':
                self._manage_customers_menu()
            elif choice == '4':
                self._manage_orders_menu()
            elif choice == '5':
                self._manage_reports_menu()
            elif choice == '6':
                print("Đã đăng xuất.")
                break
            else:
                print("❌ Lựa chọn không hợp lệ.")

    # ================= QUẢN LÝ SÁCH =================
    def _manage_books_menu(self):
        while True:
            print("\n================ QUẢN LÝ SÁCH ================")
            print("1. Thêm sách")
            print("2. Xem danh sách sách")
            print("3. Tìm kiếm sách")
            print("4. Cập nhật thông tin sách")
            print("5. Xóa sách")
            print("6. Quay lại")
            print("==============================================")
            
            choice = input("Chọn chức năng: ").strip()

            if choice == '1': self._handle_add_book()
            elif choice == '2': self._handle_view_books()
            elif choice == '3': self._handle_search_books()
            elif choice == '4': self._handle_update_book()
            elif choice == '5': self._handle_delete_book()
            elif choice == '6': break
            else: print("❌ Lựa chọn không hợp lệ.")

    def _handle_add_book(self):
        print("\n--- THÊM SÁCH MỚI ---")
        try:
            book_code = input("Mã sách (bắt buộc): ").strip()
            title = input("Tên sách (bắt buộc): ").strip()
            author = input("Tác giả (bắt buộc): ").strip()
            category = input("Thể loại: ").strip()
            publisher = input("Nhà xuất bản: ").strip()
            year_input = input("Năm xuất bản: ").strip()
            publish_year = int(year_input) if year_input else None

            if not book_code or not title or not author:
                print("❌ Lỗi: Mã sách, Tên sách và Tác giả là bắt buộc.")
                return

            new_book = Book(book_code=book_code, title=title, author=author, category=category, publisher=publisher, publish_year=publish_year)
            self.book_service.add_book(new_book)
            print("✅ Đã thêm sách thành công!")
        except ValueError as e:
            print(f"❌ Lỗi: {e}")

    def _handle_view_books(self):
        print("\n--- DANH SÁCH SÁCH ---")
        books = self.book_service.get_all_books()
        if not books: print("Không có sách nào trong hệ thống.")
        for b in books: print(f"Mã: {b.BookCode} | Tên: {b.Title} | Tác giả: {b.Author} | TT: {b.BookStatus}")

    def _handle_search_books(self):
        keyword = input("\nNhập từ khóa (Tên/Tác giả/Thể loại): ").strip()
        books = self.book_service.search_books(keyword)
        if not books: print("❌ Không tìm thấy sách phù hợp.")
        for b in books: print(f"Mã: {b.BookCode} | Tên: {b.Title} | Tác giả: {b.Author} | Thể loại: {b.Category}")

    def _handle_update_book(self):
        book_code = input("\nNhập mã sách cần cập nhật: ").strip()
        print("Nhập thông tin mới (Để trống và nhấn Enter nếu muốn giữ nguyên):")
        title = input("Tên sách mới: ").strip()
        author = input("Tác giả mới: ").strip()
        category = input("Thể loại mới: ").strip()
        publisher = input("Nhà xuất bản mới: ").strip()
        year_input = input("Năm xuất bản mới: ").strip()

        update_data = {k: v for k, v in [('Title', title), ('Author', author), ('Category', category), ('Publisher', publisher)] if v}
        if year_input.isdigit(): update_data['PublishYear'] = int(year_input)

        if not update_data:
            print("Không có thông tin nào được thay đổi.")
            return
        try:
            self.book_service.update_book(book_code, update_data)
            print(f"✅ Đã cập nhật sách {book_code} thành công!")
        except Exception as e: print(f"❌ Lỗi: {e}")

    def _handle_delete_book(self):
        book_code = input("\nNhập mã sách cần xóa: ").strip()
        try:
            if self.book_service.delete_book(book_code): print(f"✅ Đã xóa sách {book_code} thành công!")
            else: print("❌ Lỗi hệ thống khi xóa sách.")
        except ValueError as e: print(f"❌ {e}")


    # ================= QUẢN LÝ TRẠNG THÁI SÁCH =================
    def _manage_book_status_menu(self):
        while True:
            print("\n============ QUẢN LÝ TRẠNG THÁI SÁCH ============")
            print("1. Xem trạng thái tất cả sách")
            print("2. Cập nhật trạng thái sách")
            print("3. Quay lại")
            
            choice = input("Chọn chức năng: ").strip()
            if choice == '1': self._handle_view_books()
            elif choice == '2': self._handle_update_book_status()
            elif choice == '3': break
            else: print("❌ Lựa chọn không hợp lệ.")

    def _handle_update_book_status(self):
        book_code = input("\nNhập mã sách: ").strip()
        new_status = input("Nhập trạng thái mới ('Available' hoặc 'Rented'): ").strip()
        try:
            self.book_service.update_book_status(book_code, new_status)
            print("✅ Cập nhật trạng thái thành công!")
        except ValueError as e: print(f"❌ Lỗi: {e}")


    # ================= QUẢN LÝ KHÁCH HÀNG =================
    def _manage_customers_menu(self):
        while True:
            print("\n=============== QUẢN LÝ KHÁCH HÀNG ===============")
            print("1. Thêm khách hàng\n2. Xem danh sách khách hàng\n3. Tìm kiếm khách hàng\n4. Cập nhật khách hàng\n5. Xóa khách hàng\n6. Quay lại")
            choice = input("Chọn chức năng: ").strip()

            if choice == '1': self._handle_add_customer()
            elif choice == '2': self._handle_view_customers()
            elif choice == '3': self._handle_search_customers()
            elif choice == '4': self._handle_update_customer()
            elif choice == '5': self._handle_delete_customer()
            elif choice == '6': break
            else: print("❌ Lựa chọn không hợp lệ.")

    def _handle_add_customer(self):
        print("\n--- THÊM KHÁCH HÀNG ---")
        try:
            customer_code = input("Mã khách hàng (bắt buộc): ").strip()
            full_name = input("Họ tên (bắt buộc): ").strip()
            phone = input("Số điện thoại: ").strip()
            address = input("Địa chỉ: ").strip()
            email = input("Email: ").strip()

            if not customer_code or not full_name:
                print("❌ Lỗi: Mã KH và Họ tên là bắt buộc.")
                return

            new_customer = Customer(customer_code=customer_code, full_name=full_name, phone=phone, address=address, email=email)
            self.customer_service.add_customer(new_customer)
            print("✅ Đã thêm khách hàng thành công!")
        except ValueError as e: print(f"❌ Lỗi: {e}")

    def _handle_view_customers(self):
        customers = self.customer_service.get_all_customers()
        if not customers: print("\nKhông có khách hàng.")
        for c in customers: print(f"Mã KH: {c.CustomerCode} | Tên: {c.FullName} | SĐT: {c.Phone} | Email: {c.Email}")

    def _handle_search_customers(self):
        keyword = input("\nNhập từ khóa (Mã/Tên/SĐT): ").strip()
        customers = self.customer_service.search_customers(keyword)
        if not customers: print("❌ Không tìm thấy khách hàng.")
        for c in customers: print(f"Mã KH: {c.CustomerCode} | Tên: {c.FullName} | SĐT: {c.Phone}")

    def _handle_update_customer(self):
        customer_code = input("\nNhập mã KH cần cập nhật: ").strip()
        print("Nhập thông tin mới (Để trống nếu giữ nguyên):")
        update_data = {k: v for k, v in [('FullName', input("Họ tên mới: ").strip()), ('Phone', input("SĐT mới: ").strip()), 
                                         ('Address', input("Địa chỉ mới: ").strip()), ('Email', input("Email mới: ").strip())] if v}
        if not update_data: return
        try:
            self.customer_service.update_customer(customer_code, update_data)
            print(f"✅ Đã cập nhật khách hàng {customer_code}!")
        except Exception as e: print(f"❌ Lỗi: {e}")

    def _handle_delete_customer(self):
        customer_code = input("\nNhập mã KH cần xóa: ").strip()
        try:
            if self.customer_service.delete_customer(customer_code): print(f"✅ Đã xóa KH {customer_code}!")
        except ValueError as e: print(f"❌ {e}")


    # ================= QUẢN LÝ ĐƠN THUÊ =================
    def _manage_orders_menu(self):
        while True:
            print("\n================ QUẢN LÝ ĐƠN THUÊ ================")
            print("1. Tạo đơn thuê\n2. Xem danh sách đơn thuê\n3. Xem chi tiết đơn thuê\n4. Ghi nhận trả sách\n5. Quay lại")
            choice = input("Chọn chức năng: ").strip()

            if choice == '1': self._handle_create_order()
            elif choice == '2': self._handle_view_orders()
            elif choice == '3': self._handle_view_order_details()
            elif choice == '4': self._handle_return_book()
            elif choice == '5': break
            else: print("❌ Lựa chọn không hợp lệ.")

    def _handle_create_order(self):
        print("\n--- TẠO ĐƠN THUÊ ---")
        try:
            # 1. Yêu cầu nhập Mã khách hàng thay vì ID
            customer_code = input("Nhập Mã khách hàng (VD: C003): ").strip()
            
            # Tự động dò tìm CustomerID ẩn bên dưới Database
            all_customers = self.customer_service.get_all_customers()
            customer_id = None
            for c in all_customers:
                if c.CustomerCode == customer_code:
                    customer_id = c.CustomerID
                    break
            
            if not customer_id:
                print(f"❌ Lỗi: Không tìm thấy khách hàng nào có mã '{customer_code}'.")
                return

            # 2. Nhập Mã sách
            book_codes_str = input("Nhập danh sách Mã sách cần thuê (cách nhau bởi dấu phẩy, VD: IT01,LIT02): ")
            book_codes = [code.strip() for code in book_codes_str.split(",") if code.strip()]
            
            # 3. Nhập ngày trả
            date_str = input("Nhập ngày dự kiến trả (DD/MM/YYYY): ")
            expected_return_date = datetime.strptime(date_str, "%d/%m/%Y")

            # 4. Gọi Service để tạo đơn
            order_code = self.order_service.create_rental_order(
                customer_id=customer_id, 
                book_codes=book_codes, 
                expected_return_date=expected_return_date
            )
            print(f"✅ Tạo đơn thuê thành công! Mã đơn: {order_code}")
        except ValueError as e: 
            print(f"❌ Lỗi: {e}")

    def _handle_view_orders(self):
        orders = self.order_service.get_all_orders()
        if not orders: print("\nKhông có đơn thuê.")
        for o in orders: print(f"Mã đơn: {o.OrderCode} | Khách: {o.customer.FullName} | Ngày thuê: {o.RentDate.strftime('%d/%m/%Y')} | TT: {o.OrderStatus}")

    def _handle_view_order_details(self):
        order_code = input("\nNhập mã đơn thuê: ").strip()
        try:
            order = self.order_service.get_order_by_code(order_code)
            if not order:
                print("❌ Không tìm thấy đơn thuê.")
                return
            print(f"\n[Mã đơn: {order.OrderCode}] - Trạng thái: {order.OrderStatus}")
            print(f"Khách hàng: {order.customer.FullName} | Thuê: {order.RentDate.strftime('%d/%m/%Y')} | Trả dự kiến: {order.ExpectedReturnDate.strftime('%d/%m/%Y')}")
            print("Sách trong đơn:")
            for d in order.details: print(f"- {d.book.BookCode} | {d.book.Title}")
        except Exception as e: print(f"❌ Lỗi: {e}")

    def _handle_return_book(self):
        order_code = input("\nNhập mã đơn cần trả sách: ").strip()
        try:
            if self.order_service.process_return(order_code):
                print(f"✅ Đã ghi nhận trả sách cho đơn {order_code}.")
        except ValueError as e: print(f"❌ Lỗi: {e}")


    # ================= BÁO CÁO =================
    def _manage_reports_menu(self):
        while True:
            print("\n==================== BÁO CÁO ====================")
            print("1. Thống kê sách đang được thuê\n2. Thống kê sách có sẵn\n3. Thống kê số lượt thuê theo sách\n4. Quay lại")
            choice = input("Chọn chức năng: ").strip()

            if choice in ['1', '2']:
                stats = self.report_service.get_inventory_stats()
                if choice == '1': print(f"\n📊 Tổng sách ĐANG THUÊ: {stats['Rented']} cuốn.")
                else: print(f"\n📊 Tổng sách CÓ SẴN: {stats['Available']} cuốn.")
            elif choice == '3':
                try:
                    stats = self.report_service.get_book_rental_frequency()
                    if not stats: print("Chưa có dữ liệu.")
                    for s in stats: print(f"Mã: {s['BookCode']} | Tên: {s['Title']} | Lượt thuê: {s['RentalCount']}")
                except Exception as e: print(f"❌ Lỗi: {e}")
            elif choice == '4': break
            else: print("❌ Lựa chọn không hợp lệ.")