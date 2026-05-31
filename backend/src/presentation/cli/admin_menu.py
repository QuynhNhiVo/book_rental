"""Admin Menu - Administrative operations for Book Rental System"""
from datetime import datetime
from domain.models.book import Book
from domain.models.customer import Customer
from domain.exceptions.business_exception import (
    BookNotFoundError, CustomerNotFoundError, OrderNotFoundError,
    BookCannotBeDeletedError, CustomerHasActiveOrderError, DuplicateCodeError,
    BookNotAvailableError, UnauthorizedError
)


class AdminMenu:
    """Admin menu for managing books, customers, orders, and reports"""
    
    def __init__(self, user, services: dict):
        if user.role != 'Admin':
            raise UnauthorizedError('Access denied. Admin role is required to use the admin menu.')
        self.user = user
        self.book_service = services.get('book')
        self.order_service = services.get('order')
        self.customer_service = services.get('customer')
        self.report_service = services.get('report')
    
    def display(self):
        """Display admin menu loop"""
        while True:
            self._print_admin_menu()
            choice = input("Chọn chức năng: ").strip()
            
            if choice == '1':
                self._manage_books_menu()
            elif choice == '2':
                self._manage_customers_menu()
            elif choice == '3':
                self._manage_orders_menu()
            elif choice == '4':
                self._manage_reports_menu()
            elif choice == '5':
                self._manage_book_status_menu()
            elif choice == '6':
                print("\n✅ Đã đăng xuất. Tạm biệt!")
                break
            else:
                print("\n❌ Lựa chọn không hợp lệ. Vui lòng thử lại.")
    
    def _print_admin_menu(self):
        """Print admin menu"""
        print("\n" + "="*60)
        print(f"📋 MENU QUẢN TRỊ VIÊN ({self.user.username})")
        print("="*60)
        print("1. 📚 Quản lý sách")
        print("2. 👥 Quản lý khách hàng")
        print("3. 📦 Quản lý đơn thuê")
        print("4. 📊 Báo cáo thống kê")
        print("5. 🔧 Quản lý trạng thái sách")
        print("6. 🚪 Đăng xuất")
        print("="*60)
    
    # ==================== QUẢN LÝ SÁCH ====================
    
    def _manage_books_menu(self):
        """Book management submenu"""
        while True:
            print("\n" + "-"*60)
            print("📚 QUẢN LÝ SÁCH")
            print("-"*60)
            print("1. ➕ Thêm sách mới")
            print("2. 👁️  Xem danh sách sách")
            print("3. 🔍 Tìm kiếm sách")
            print("4. ✏️  Cập nhật thông tin sách")
            print("5. ❌ Xóa sách")
            print("6. 📊 Xem trạng thái sách")
            print("7. ↩️  Quay lại")
            print("-"*60)
            
            choice = input("Chọn chức năng: ").strip()
            
            if choice == '1':
                self._handle_add_book()
            elif choice == '2':
                self._handle_view_all_books()
            elif choice == '3':
                self._handle_search_books()
            elif choice == '4':
                self._handle_update_book()
            elif choice == '5':
                self._handle_delete_book()
            elif choice == '6':
                self._handle_view_book_status()
            elif choice == '7':
                break
            else:
                print("❌ Lựa chọn không hợp lệ.")
    
    def _handle_add_book(self):
        """Add new book"""
        print("\n" + "="*60)
        print("➕ THÊM SÁCH MỚI")
        print("="*60)
        
        try:
            book_code = input("Mã sách (bắt buộc): ").strip()
            title = input("Tên sách (bắt buộc): ").strip()
            author = input("Tác giả (bắt buộc): ").strip()
            category = input("Thể loại: ").strip() or None
            publisher = input("Nhà xuất bản: ").strip() or None
            
            year_input = input("Năm xuất bản: ").strip()
            publish_year = int(year_input) if year_input else None
            
            if not book_code or not title or not author:
                print("❌ Lỗi: Mã sách, tên sách và tác giả là bắt buộc.")
                return
            
            new_book = Book(
                book_code=book_code,
                title=title,
                author=author,
                category=category,
                publisher=publisher,
                publish_year=publish_year
            )
            
            book_id = self.book_service.create_book(new_book)
            print(f"\n✅ Thêm sách thành công!")
            print(f"   Mã sách: {book_code}")
            print(f"   Tên sách: {title}")
            
        except DuplicateCodeError as e:
            print(f"\n❌ Lỗi: {e.message}")
        except Exception as e:
            print(f"\n❌ Lỗi: {str(e)}")
    
    def _handle_view_all_books(self):
        """View all books with formatted table"""
        print("\n" + "="*80)
        print("📚 DANH SÁCH TẤT CẢ SÁCH")
        print("="*80)
        
        try:
            books = self.book_service.get_all_books()
            
            if not books:
                print("Hệ thống chưa có sách nào.")
                return
            
            self._print_books_table(books)
            print(f"\nTổng cộng: {len(books)} cuốn sách")
            
        except Exception as e:
            print(f"❌ Lỗi: {str(e)}")
    
    def _handle_search_books(self):
        """Search books by keyword"""
        print("\n" + "="*60)
        print("🔍 TÌM KIẾM SÁCH")
        print("="*60)
        
        keyword = input("Nhập từ khóa (tên/tác giả/thể loại): ").strip()
        
        if not keyword:
            print("❌ Từ khóa không được để trống.")
            return
        
        try:
            books = self.book_service.search_books(keyword)
            
            if not books:
                print(f"\n❌ Không tìm thấy sách nào chứa '{keyword}'.")
                return
            
            print(f"\n✅ Tìm thấy {len(books)} cuốn sách:")
            self._print_books_table(books)
            
        except Exception as e:
            print(f"❌ Lỗi: {str(e)}")
    
    def _handle_update_book(self):
        """Update book information"""
        print("\n" + "="*60)
        print("✏️  CẬP NHẬT THÔNG TIN SÁCH")
        print("="*60)
        
        book_code = input("Nhập mã sách cần cập nhật: ").strip()
        
        if not book_code:
            print("❌ Mã sách không được để trống.")
            return
        
        try:
            existing_book = self.book_service.get_book_by_code(book_code)
            
            print(f"\nThông tin hiện tại của sách '{book_code}':")
            print(f"  Tên: {existing_book.title}")
            print(f"  Tác giả: {existing_book.author}")
            print(f"  Thể loại: {existing_book.category or '(Chưa có)'}")
            print(f"  Nhà xuất bản: {existing_book.publisher or '(Chưa có)'}")
            print(f"  Năm xuất bản: {existing_book.publish_year or '(Chưa có)'}")
            
            print("\nNhập thông tin mới (để trống để giữ nguyên):")
            title = input("Tên sách mới: ").strip() or existing_book.title
            author = input("Tác giả mới: ").strip() or existing_book.author
            category = input("Thể loại mới: ").strip() or existing_book.category
            publisher = input("Nhà xuất bản mới: ").strip() or existing_book.publisher
            
            year_input = input("Năm xuất bản mới: ").strip()
            publish_year = int(year_input) if year_input else existing_book.publish_year
            
            updated_book = Book(
                book_code=book_code,
                title=title,
                author=author,
                category=category,
                publisher=publisher,
                publish_year=publish_year,
                book_id=existing_book.book_id,
                book_status=existing_book.book_status
            )
            
            self.book_service.update_book(updated_book)
            print(f"\n✅ Cập nhật sách '{book_code}' thành công!")
            
        except BookNotFoundError as e:
            print(f"\n❌ {e.message}")
        except Exception as e:
            print(f"\n❌ Lỗi: {str(e)}")
    
    def _handle_delete_book(self):
        """Delete book (only if available)"""
        print("\n" + "="*60)
        print("❌ XÓA SÁCH")
        print("="*60)
        print("⚠️  Chỉ có thể xóa sách ở trạng thái 'Có sẵn'")
        
        book_code = input("\nNhập mã sách cần xóa: ").strip()
        
        if not book_code:
            print("❌ Mã sách không được để trống.")
            return
        
        try:
            book = self.book_service.get_book_by_code(book_code)
            
            print(f"\nThông tin sách sẽ xóa:")
            print(f"  Mã: {book.book_code}")
            print(f"  Tên: {book.title}")
            print(f"  Trạng thái: {book.book_status}")
            
            confirm = input("\nBạn chắc chắn muốn xóa sách này? (yes/no): ").strip().lower()
            
            if confirm != 'yes':
                print("❌ Xóa bị hủy.")
                return
            
            self.book_service.delete_book(book.book_id)
            print(f"\n✅ Xóa sách '{book_code}' thành công!")
            
        except BookNotFoundError as e:
            print(f"\n❌ {e.message}")
        except BookCannotBeDeletedError as e:
            print(f"\n❌ {e.message}")
        except Exception as e:
            print(f"\n❌ Lỗi: {str(e)}")
    
    def _handle_view_book_status(self):
        """View book status overview"""
        print("\n" + "="*80)
        print("📊 TRẠNG THÁI SÁCH")
        print("="*80)
        
        try:
            books = self.book_service.get_all_books()
            
            if not books:
                print("Hệ thống chưa có sách nào.")
                return
            
            available = [b for b in books if b.book_status == 'Available']
            rented = [b for b in books if b.book_status == 'Rented']
            damaged = [b for b in books if b.book_status == 'Damaged']
            lost = [b for b in books if b.book_status == 'Lost']
            
            print(f"\n📊 Thống kê chung:")
            print(f"  Tổng số sách: {len(books)}")
            print(f"  ✅ Có sẵn: {len(available)}")
            print(f"  📤 Đang thuê: {len(rented)}")
            print(f"  ⚠️  Hỏng: {len(damaged)}")
            print(f"  ❌ Mất: {len(lost)}")
            
            print(f"\n📚 Sách đang thuê ({len(rented)} cuốn):")
            if rented:
                self._print_books_table(rented)
            else:
                print("  (Không có)")
            
        except Exception as e:
            print(f"❌ Lỗi: {str(e)}")
    
    def _manage_book_status_menu(self):
        """Manage book status (Available, Rented, Damaged, Lost)"""
        while True:
            print("\n" + "-"*60)
            print("🔧 QUẢN LÝ TRẠNG THÁI SÁCH")
            print("-"*60)
            print("1. 📋 Xem sách theo trạng thái")
            print("2. 🔄 Cập nhật trạng thái sách")
            print("3. ↩️  Quay lại")
            print("-"*60)
            
            choice = input("Chọn chức năng: ").strip()
            
            if choice == '1':
                self._handle_view_books_by_status()
            elif choice == '2':
                self._handle_update_book_status()
            elif choice == '3':
                break
            else:
                print("❌ Lựa chọn không hợp lệ.")
    
    def _handle_view_books_by_status(self):
        """View books filtered by status"""
        print("\n" + "="*60)
        print("📋 XEM SÁCH THEO TRẠNG THÁI")
        print("="*60)
        print("1. ✅ Có sẵn")
        print("2. 📤 Đang thuê")
        print("3. ⚠️  Hỏng")
        print("4. ❌ Mất")
        
        status_choice = input("\nChọn trạng thái: ").strip()
        
        status_map = {
            '1': 'Available',
            '2': 'Rented',
            '3': 'Damaged',
            '4': 'Lost'
        }
        
        if status_choice not in status_map:
            print("❌ Lựa chọn không hợp lệ.")
            return
        
        try:
            books = self.book_service.get_all_books()
            filtered = [b for b in books if b.book_status == status_map[status_choice]]
            
            if not filtered:
                print(f"\nKhông có sách nào ở trạng thái '{status_map[status_choice]}'")
                return
                return
            
            print(f"\n✅ Tìm thấy {len(filtered)} cuốn sách:")
            self._print_books_table(filtered)
            
        except Exception as e:
            print(f"❌ Lỗi: {str(e)}")
    
    def _handle_update_book_status(self):
        """Update book status"""
        print("\n" + "="*60)
        print("🔄 CẬP NHẬT TRẠNG THÁI SÁCH")
        print("="*60)
        
        book_code = input("Nhập mã sách: ").strip()
        
        if not book_code:
            print("❌ Mã sách không được để trống.")
            return
        
        print("\nTrạng thái sách:")
        print("1. ✅ Available (Có sẵn)")
        print("2. 📤 Rented (Đang thuê)")
        print("3. ⚠️  Damaged (Hỏng)")
        print("4. ❌ Lost (Mất)")
        
        status_choice = input("\nChọn trạng thái mới: ").strip()
        
        status_map = {
            '1': 'Available',
            '2': 'Rented',
            '3': 'Damaged',
            '4': 'Lost'
        }
        
        if status_choice not in status_map:
            print("❌ Lựa chọn không hợp lệ.")
            return
        
        try:
            book = self.book_service.get_book_by_code(book_code)
            self.book_service.update_book_status(book.book_id, status_map[status_choice])
            print(f"\n✅ Cập nhật trạng thái sách '{book_code}' thành '{status_map[status_choice]}' thành công!")
            
        except BookNotFoundError as e:
            print(f"\n❌ {e.message}")
        except Exception as e:
            print(f"\n❌ Lỗi: {str(e)}")
    
    # ==================== QUẢN LÝ KHÁCH HÀNG ====================
    
    def _manage_customers_menu(self):
        """Customer management submenu"""
        while True:
            print("\n" + "-"*60)
            print("👥 QUẢN LÝ KHÁCH HÀNG")
            print("-"*60)
            print("1. ➕ Thêm khách hàng mới")
            print("2. 👁️  Xem danh sách khách hàng")
            print("3. 🔍 Tìm kiếm khách hàng")
            print("4. ✏️  Cập nhật thông tin khách hàng")
            print("5. ❌ Xóa khách hàng")
            print("6. 📊 Xem đơn thuê của khách hàng")
            print("7. ↩️  Quay lại")
            print("-"*60)
            
            choice = input("Chọn chức năng: ").strip()
            
            if choice == '1':
                self._handle_add_customer()
            elif choice == '2':
                self._handle_view_all_customers()
            elif choice == '3':
                self._handle_search_customers()
            elif choice == '4':
                self._handle_update_customer()
            elif choice == '5':
                self._handle_delete_customer()
            elif choice == '6':
                self._handle_view_customer_orders()
            elif choice == '7':
                break
            else:
                print("❌ Lựa chọn không hợp lệ.")
    
    def _handle_add_customer(self):
        """Add new customer"""
        print("\n" + "="*60)
        print("➕ THÊM KHÁCH HÀNG MỚI")
        print("="*60)
        
        try:
            customer_code = input("Mã khách hàng (bắt buộc): ").strip()
            fullname = input("Họ tên (bắt buộc): ").strip()
            phone = input("Số điện thoại: ").strip() or None
            address = input("Địa chỉ: ").strip() or None
            email = input("Email: ").strip() or None
            
            if not customer_code or not fullname:
                print("❌ Lỗi: Mã khách hàng và họ tên là bắt buộc.")
                return
            
            new_customer = Customer(
                customer_code=customer_code,
                fullname=fullname,
                phone=phone,
                address=address,
                email=email
            )
            
            customer_id = self.customer_service.create_customer(new_customer)
            print(f"\n✅ Thêm khách hàng thành công!")
            print(f"   Mã khách: {customer_code}")
            print(f"   Tên: {fullname}")
            
        except DuplicateCodeError as e:
            print(f"\n❌ Lỗi: {e.message}")
        except Exception as e:
            print(f"\n❌ Lỗi: {str(e)}")
    
    def _handle_view_all_customers(self):
        """View all customers"""
        print("\n" + "="*100)
        print("👥 DANH SÁCH TẤT CẢ KHÁCH HÀNG")
        print("="*100)
        
        try:
            customers = self.customer_service.get_all_customers()
            
            if not customers:
                print("Hệ thống chưa có khách hàng nào.")
                return
            
            self._print_customers_table(customers)
            print(f"\nTổng cộng: {len(customers)} khách hàng")
            
        except Exception as e:
            print(f"❌ Lỗi: {str(e)}")
    
    def _handle_search_customers(self):
        """Search customers"""
        print("\n" + "="*60)
        print("🔍 TÌM KIẾM KHÁCH HÀNG")
        print("="*60)
        
        keyword = input("Nhập từ khóa (mã/tên/sđt): ").strip()
        
        if not keyword:
            print("❌ Từ khóa không được để trống.")
            return
        
        try:
            customers = self.customer_service.search_customers(keyword)
            
            if not customers:
                print(f"\n❌ Không tìm thấy khách hàng nào chứa '{keyword}'.")
                return
            
            print(f"\n✅ Tìm thấy {len(customers)} khách hàng:")
            self._print_customers_table(customers)
            
        except Exception as e:
            print(f"❌ Lỗi: {str(e)}")
    
    def _handle_update_customer(self):
        """Update customer information"""
        print("\n" + "="*60)
        print("✏️  CẬP NHẬT THÔNG TIN KHÁCH HÀNG")
        print("="*60)
        
        customer_code = input("Nhập mã khách hàng cần cập nhật: ").strip()
        
        if not customer_code:
            print("❌ Mã khách hàng không được để trống.")
            return
        
        try:
            existing_customer = self.customer_service.get_customer_by_code(customer_code)
            
            print(f"\nThông tin hiện tại của khách hàng '{customer_code}':")
            print(f"  Tên: {existing_customer.fullname}")
            print(f"  SĐT: {existing_customer.phone or '(Chưa có)'}")
            print(f"  Địa chỉ: {existing_customer.address or '(Chưa có)'}")
            print(f"  Email: {existing_customer.email or '(Chưa có)'}")
            
            print("\nNhập thông tin mới (để trống để giữ nguyên):")
            fullname = input("Họ tên mới: ").strip() or existing_customer.fullname
            phone = input("SĐT mới: ").strip() or existing_customer.phone
            address = input("Địa chỉ mới: ").strip() or existing_customer.address
            email = input("Email mới: ").strip() or existing_customer.email
            
            updated_customer = Customer(
                customer_code=customer_code,
                fullname=fullname,
                phone=phone,
                address=address,
                email=email,
                customer_id=existing_customer.customer_id
            )
            
            self.customer_service.update_customer(updated_customer)
            print(f"\n✅ Cập nhật khách hàng '{customer_code}' thành công!")
            
        except CustomerNotFoundError as e:
            print(f"\n❌ {e.message}")
        except Exception as e:
            print(f"\n❌ Lỗi: {str(e)}")
    
    def _handle_delete_customer(self):
        """Delete customer (only if no active rentals)"""
        print("\n" + "="*60)
        print("❌ XÓA KHÁCH HÀNG")
        print("="*60)
        print("⚠️  Chỉ có thể xóa khách hàng không có đơn thuê đang hoạt động")
        
        customer_code = input("\nNhập mã khách hàng cần xóa: ").strip()
        
        if not customer_code:
            print("❌ Mã khách hàng không được để trống.")
            return
        
        try:
            customer = self.customer_service.get_customer_by_code(customer_code)
            
            print(f"\nThông tin khách hàng sẽ xóa:")
            print(f"  Mã: {customer.customer_code}")
            print(f"  Tên: {customer.fullname}")
            
            confirm = input("\nBạn chắc chắn muốn xóa khách hàng này? (yes/no): ").strip().lower()
            
            if confirm != 'yes':
                print("❌ Xóa bị hủy.")
                return
            
            self.customer_service.delete_customer(customer.customer_id)
            print(f"\n✅ Xóa khách hàng '{customer_code}' thành công!")
            
        except CustomerNotFoundError as e:
            print(f"\n❌ {e.message}")
        except CustomerHasActiveOrderError as e:
            print(f"\n❌ {e.message}")
        except Exception as e:
            print(f"\n❌ Lỗi: {str(e)}")
    
    def _handle_view_customer_orders(self):
        """View customer's rental orders"""
        print("\n" + "="*60)
        print("📊 XEM ĐƠN THUÊ CỦA KHÁCH HÀNG")
        print("="*60)
        
        customer_code = input("Nhập mã khách hàng: ").strip()
        
        if not customer_code:
            print("❌ Mã khách hàng không được để trống.")
            return
        
        try:
            customer = self.customer_service.get_customer_by_code(customer_code)
            orders = self.order_service.get_customer_all_orders(customer.customer_id)
            
            if not orders:
                print(f"\n❌ Khách hàng '{customer_code}' chưa có đơn thuê nào.")
                return
            
            print(f"\n✅ Khách hàng '{customer_code}' - {customer.fullname} có {len(orders)} đơn thuê:")
            self._print_orders_table(orders)
            
        except CustomerNotFoundError as e:
            print(f"\n❌ {e.message}")
        except Exception as e:
            print(f"\n❌ Lỗi: {str(e)}")
    
    # ==================== QUẢN LÝ ĐƠN THUÊ ====================
    
    def _manage_orders_menu(self):
        """Order management submenu"""
        while True:
            print("\n" + "-"*60)
            print("📦 QUẢN LÝ ĐƠN THUÊ")
            print("-"*60)
            print("1. ➕ Tạo đơn thuê mới")
            print("2. 👁️  Xem danh sách đơn thuê")
            print("3. 📋 Xem chi tiết đơn thuê")
            print("4. 📤 Ghi nhận trả sách")
            print("5. ↩️  Quay lại")
            print("-"*60)
            
            choice = input("Chọn chức năng: ").strip()
            
            if choice == '1':
                self._handle_create_order()
            elif choice == '2':
                self._handle_view_all_orders()
            elif choice == '3':
                self._handle_view_order_details()
            elif choice == '4':
                self._handle_return_books()
            elif choice == '5':
                break
            else:
                print("❌ Lựa chọn không hợp lệ.")
    
    def _handle_create_order(self):
        """Create new rental order"""
        print("\n" + "="*60)
        print("➕ TẠO ĐƠN THUÊ MỚI")
        print("="*60)
        
        try:
            customer_code = input("Nhập mã khách hàng: ").strip()
            
            if not customer_code:
                print("❌ Mã khách hàng không được để trống.")
                return
            
            customer = self.customer_service.get_customer_by_code(customer_code)
            
            print(f"\n✅ Khách hàng: {customer.fullname}")
            print("\nNhập danh sách mã sách muốn thuê (cách nhau bằng dấu phẩy):")
            print("Ví dụ: BOOK01,BOOK02,BOOK03")
            
            book_codes_str = input("Danh sách mã sách: ").strip()
            book_codes = [code.strip() for code in book_codes_str.split(",") if code.strip()]
            
            if not book_codes:
                print("❌ Phải chọn ít nhất một cuốn sách.")
                return
            
            print("\nNhập ngày dự kiến trả sách:")
            date_str = input("Ngày trả (DD/MM/YYYY): ").strip()
            expected_return_date = datetime.strptime(date_str, "%d/%m/%Y")
            
            order_id = self.order_service.create_rental_order(
                customer_id=customer.customer_id,
                book_codes=book_codes,
                expected_return_date=expected_return_date
            )
            
            print(f"\n✅ Tạo đơn thuê thành công!")
            print(f"   Khách hàng: {customer.fullname}")
            print(f"   Số lượng sách: {len(book_codes)}")
            print(f"   Ngày dự kiến trả: {expected_return_date.strftime('%d/%m/%Y')}")
            
        except CustomerNotFoundError as e:
            print(f"\n❌ {e.message}")
        except BookNotFoundError as e:
            print(f"\n❌ {e.message}")
        except BookNotAvailableError as e:
            print(f"\n❌ {e.message}")
        except ValueError as e:
            print(f"\n❌ Lỗi định dạng ngày: {str(e)}")
        except Exception as e:
            print(f"\n❌ Lỗi: {str(e)}")
    
    def _handle_view_all_orders(self):
        """View all orders"""
        print("\n" + "="*100)
        print("📦 DANH SÁCH TẤT CẢ ĐƠN THUÊ")
        print("="*100)
        
        try:
            orders = self.order_service.get_all_orders()
            
            if not orders:
                print("Hệ thống chưa có đơn thuê nào.")
                return
            
            self._print_orders_table(orders)
            
            renting = sum(1 for o in orders if o.order_status == 'Renting')
            returned = sum(1 for o in orders if o.order_status == 'Returned')
            
            print(f"\nThống kê:")
            print(f"  Đang thuê: {renting}")
            print(f"  Đã trả: {returned}")
            print(f"  Tổng cộng: {len(orders)}")
            
        except Exception as e:
            print(f"❌ Lỗi: {str(e)}")
    
    def _handle_view_order_details(self):
        """View order details"""
        print("\n" + "="*60)
        print("📋 XEM CHI TIẾT ĐƠN THUÊ")
        print("="*60)
        
        order_code = input("Nhập mã đơn thuê: ").strip()
        
        if not order_code:
            print("❌ Mã đơn thuê không được để trống.")
            return
        
        try:
            order = self.order_service.get_order_by_code(order_code)
            details = self.order_service.get_order_details(order.order_id)
            
            print(f"\n📋 Đơn thuê: {order.order_code}")
            print(f"   Trạng thái: {order.order_status}")
            print(f"   Ngày thuê: {order.rent_date.strftime('%d/%m/%Y')}")
            print(f"   Ngày dự kiến trả: {order.expected_return_date.strftime('%d/%m/%Y')}")
            if order.return_date:
                print(f"   Ngày trả thực tế: {order.return_date.strftime('%d/%m/%Y')}")
            
            print(f"\n📚 Sách trong đơn ({len(details)} cuốn):")
            print("-" * 80)
            print(f"{'STT':<5} | {'Mã Sách':<15} | {'Tên Sách':<50} | {'Tác Giả':<20}")
            print("-" * 80)
            
            for i, detail in enumerate(details, 1):
                print(f"{i:<5} | {detail.book_code:<15} | {detail.title:<50} | {detail.author:<20}")
            
        except OrderNotFoundError as e:
            print(f"\n❌ {e.message}")
        except Exception as e:
            print(f"\n❌ Lỗi: {str(e)}")
    
    def _handle_return_books(self):
        """Process book return"""
        print("\n" + "="*60)
        print("📤 GHI NHẬN TRẢ SÁCH")
        print("="*60)
        
        order_code = input("Nhập mã đơn thuê cần trả: ").strip()
        
        if not order_code:
            print("❌ Mã đơn thuê không được để trống.")
            return
        
        try:
            order = self.order_service.get_order_by_code(order_code)
            
            if order.order_status != 'Renting':
                print(f"\n❌ Lỗi: Đơn thuê này không ở trạng thái 'Đang thuê' (hiện tại: {order.order_status})")
                return
            
            details = self.order_service.get_order_details(order.order_id)
            
            print(f"\n📋 Xác nhận trả sách:")
            print(f"   Mã đơn: {order.order_code}")
            print(f"   Số sách: {len(details)}")
            
            for detail in details:
                print(f"   - {detail.book_code} | {detail.title}")
            
            confirm = input("\nBạn chắc chắn muốn ghi nhận trả sách? (yes/no): ").strip().lower()
            
            if confirm != 'yes':
                print("❌ Ghi nhận trả sách bị hủy.")
                return
            
            self.order_service.process_return(order.order_id)
            print(f"\n✅ Ghi nhận trả sách thành công!")
            print(f"   Đơn {order.order_code} đã được đánh dấu là 'Đã trả'")
            
        except OrderNotFoundError as e:
            print(f"\n❌ {e.message}")
        except Exception as e:
            print(f"\n❌ Lỗi: {str(e)}")
    
    # ==================== BÁO CÁO THỐNG KÊ ====================
    
    def _manage_reports_menu(self):
        """Reports submenu"""
        while True:
            print("\n" + "-"*60)
            print("📊 BÁO CÁO THỐNG KÊ")
            print("-"*60)
            print("1. 📚 Thống kê sách")
            print("2. 📤 Thống kê đơn thuê")
            print("3. 📈 Thống kê tổng hợp")
            print("4. ↩️  Quay lại")
            print("-"*60)
            
            choice = input("Chọn chức năng: ").strip()
            
            if choice == '1':
                self._handle_book_statistics()
            elif choice == '2':
                self._handle_rental_statistics()
            elif choice == '3':
                self._handle_overall_statistics()
            elif choice == '4':
                break
            else:
                print("❌ Lựa chọn không hợp lệ.")
    
    def _handle_book_statistics(self):
        """View book statistics"""
        print("\n" + "="*60)
        print("📚 THỐNG KÊ SÁCH")
        print("="*60)
        
        try:
            books = self.book_service.get_all_books()
            
            available = len([b for b in books if b.book_status == 'Available'])
            rented = len([b for b in books if b.book_status == 'Rented'])
            damaged = len([b for b in books if b.book_status == 'Damaged'])
            lost = len([b for b in books if b.book_status == 'Lost'])
            
            print(f"\n📊 Tổng số sách: {len(books)}")
            print(f"   ✅ Có sẵn: {available} ({available*100//len(books) if books else 0}%)")
            print(f"   📤 Đang thuê: {rented} ({rented*100//len(books) if books else 0}%)")
            print(f"   ⚠️  Hỏng: {damaged} ({damaged*100//len(books) if books else 0}%)")
            print(f"   ❌ Mất: {lost} ({lost*100//len(books) if books else 0}%)")
            
        except Exception as e:
            print(f"❌ Lỗi: {str(e)}")
    
    def _handle_rental_statistics(self):
        """View rental statistics"""
        print("\n" + "="*60)
        print("📤 THỐNG KÊ ĐƠN THUÊ")
        print("="*60)
        
        try:
            orders = self.order_service.get_all_orders()
            
            renting = len([o for o in orders if o.order_status == 'Renting'])
            returned = len([o for o in orders if o.order_status == 'Returned'])
            
            print(f"\n📊 Tổng đơn thuê: {len(orders)}")
            print(f"   📤 Đang thuê: {renting} ({renting*100//len(orders) if orders else 0}%)")
            print(f"   ✅ Đã trả: {returned} ({returned*100//len(orders) if orders else 0}%)")
            
            if orders:
                total_books = sum(len(self.order_service.get_order_details(o.order_id)) for o in orders)
                print(f"   📚 Tổng số lần mượn: {total_books}")
            
        except Exception as e:
            print(f"❌ Lỗi: {str(e)}")
    
    def _handle_overall_statistics(self):
        """View overall statistics"""
        print("\n" + "="*80)
        print("📈 THỐNG KÊ TỔNG HỢP")
        print("="*80)
        
        try:
            books = self.book_service.get_all_books()
            customers = self.customer_service.get_all_customers()
            orders = self.order_service.get_all_orders()
            
            available = len([b for b in books if b.book_status == 'Available'])
            rented = len([b for b in books if b.book_status == 'Rented'])
            renting_orders = len([o for o in orders if o.order_status == 'Renting'])
            returned_orders = len([o for o in orders if o.order_status == 'Returned'])
            
            print(f"\n📚 SỰ KIỆN SÁCH:")
            print(f"   Tổng sách: {len(books)}")
            print(f"   Có sẵn: {available}")
            print(f"   Đang thuê: {rented}")
            
            print(f"\n👥 KHÁCH HÀNG:")
            print(f"   Tổng khách hàng: {len(customers)}")
            
            print(f"\n📦 ĐƠN THUÊ:")
            print(f"   Tổng đơn: {len(orders)}")
            print(f"   Đang thuê: {renting_orders}")
            print(f"   Đã trả: {returned_orders}")
            
            if orders:
                total_rental_items = sum(len(self.order_service.get_order_details(o.order_id)) for o in orders)
                avg_books_per_order = total_rental_items / len(orders)
                print(f"   Trung bình sách/đơn: {avg_books_per_order:.1f}")
            
        except Exception as e:
            print(f"❌ Lỗi: {str(e)}")
    
    # ==================== HELPER METHODS ====================
    
    def _print_books_table(self, books):
        """Print formatted books table"""
        print("-" * 100)
        print(f"{'STT':<5} | {'Mã Sách':<12} | {'Tên Sách':<40} | {'Tác Giả':<20} | {'Trạng Thái':<12}")
        print("-" * 100)
        
        for i, book in enumerate(books, 1):
            status_display = {
                'Available': '✅ Có sẵn',
                'Rented': '📤 Đang thuê',
                'Damaged': '⚠️  Hỏng',
                'Lost': '❌ Mất'
            }.get(book.book_status, book.book_status)
            
            print(f"{i:<5} | {book.book_code:<12} | {book.title[:40]:<40} | {book.author[:20]:<20} | {status_display:<12}")
    
    def _print_customers_table(self, customers):
        """Print formatted customers table"""
        print("-" * 120)
        print(f"{'STT':<5} | {'Mã KH':<12} | {'Họ Tên':<30} | {'Số ĐT':<15} | {'Email':<35}")
        print("-" * 120)
        
        for i, customer in enumerate(customers, 1):
            print(f"{i:<5} | {customer.customer_code:<12} | {customer.fullname[:30]:<30} | {str(customer.phone or ''):<15} | {customer.email or '':<35}")
    
    def _print_orders_table(self, orders):
        """Print formatted orders table"""
        print("-" * 120)
        print(f"{'STT':<5} | {'Mã Đơn':<15} | {'Mã KH':<12} | {'Ngày Thuê':<15} | {'Ngày Trả DK':<15} | {'Trạng Thái':<12}")
        print("-" * 120)
        
        for i, order in enumerate(orders, 1):
            customer = self.customer_service.get_customer_by_id(order.customer_id)
            status_display = {
                'Renting': '📤 Đang thuê',
                'Returned': '✅ Đã trả'
            }.get(order.order_status, order.order_status)
            
            print(f"{i:<5} | {order.order_code:<15} | {customer.customer_code:<12} | {order.rent_date.strftime('%d/%m/%Y'):<15} | {order.expected_return_date.strftime('%d/%m/%Y'):<15} | {status_display:<12}")