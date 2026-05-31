"""Customer Menu - Customer operations for Book Rental System"""
from datetime import datetime
from domain.exceptions.business_exception import (
    BookNotFoundError, CustomerNotFoundError, OrderNotFoundError,
    BookNotAvailableError, InvalidDateError, UnauthorizedError
)


class CustomerMenu:
    """Customer menu for searching, renting books, and viewing orders"""
    
    def __init__(self, user, services: dict):
        if user.role != 'Customer':
            raise UnauthorizedError('Access denied. Customer role is required to use the customer menu.')
        self.user = user
        self.book_service = services.get('book')
        self.order_service = services.get('order')
        self.customer_service = services.get('customer')
    
    def display(self):
        """Display customer menu loop"""
        # Get customer info
        try:
            customer = self.customer_service.get_customer_by_id(self.user.customer_id)
            customer_name = customer.fullname
        except:
            customer_name = self.user.username
        
        while True:
            self._print_customer_menu(customer_name)
            choice = input("Chọn chức năng: ").strip()
            
            if choice == '1':
                self._handle_search_books()
            elif choice == '2':
                self._handle_view_all_books()
            elif choice == '3':
                self._handle_rent_books()
            elif choice == '4':
                self._handle_view_renting_orders()
            elif choice == '5':
                self._handle_view_all_orders()
            elif choice == '6':
                print("\n✅ Đã đăng xuất. Tạm biệt!")
                break
            else:
                print("\n❌ Lựa chọn không hợp lệ. Vui lòng thử lại.")
    
    def _print_customer_menu(self, customer_name):
        """Print customer menu"""
        print("\n" + "="*80)
        print(f"📚 MENU KHÁCH HÀNG ({customer_name})")
        print("="*80)
        print("1. 🔍 Tìm kiếm sách")
        print("2. 👁️  Xem toàn bộ sách trong thư viện")
        print("3. 🛒 Thuê sách")
        print("4. 📤 Xem sách đang thuê")
        print("5. 📋 Xem lịch sử thuê sách")
        print("6. 🚪 Đăng xuất")
        print("="*80)
    
    # ==================== TÌM KIẾM SÁCH ====================
    
    def _handle_search_books(self):
        """Search books by keyword"""
        print("\n" + "="*80)
        print("🔍 TÌM KIẾM SÁCH")
        print("="*80)
        print("Bạn có thể tìm kiếm theo: Tên sách, Tác giả, Thể loại")
        
        keyword = input("\nNhập từ khóa: ").strip()
        
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
            
            # Show only available books count
            available = len([b for b in books if b.book_status == 'Available'])
            print(f"\n📊 Trong đó {available} cuốn có sẵn để thuê")
            
        except Exception as e:
            print(f"\n❌ Lỗi: {str(e)}")
    
    # ==================== XEM SÁCH ====================
    
    def _handle_view_all_books(self):
        """View all books in library"""
        print("\n" + "="*80)
        print("👁️  DANH SÁCH TẤT CẢ SÁCH TRONG THƯ VIỆN")
        print("="*80)
        
        try:
            books = self.book_service.get_all_books()
            
            if not books:
                print("\nThư viện chưa có sách nào.")
                return
            
            available = [b for b in books if b.book_status == 'Available']
            
            print(f"\n📊 Thống kê sách:")
            print(f"   Tổng sách: {len(books)}")
            print(f"   ✅ Có sẵn để thuê: {len(available)}")
            print(f"   📤 Đang được thuê: {len(books) - len(available)}")
            
            print(f"\n📚 Danh sách tất cả sách:")
            self._print_books_table(books)
            
        except Exception as e:
            print(f"\n❌ Lỗi: {str(e)}")
    
    # ==================== THUÊ SÁCH ====================
    
    def _handle_rent_books(self):
        """Rent books"""
        print("\n" + "="*80)
        print("🛒 THUÊ SÁCH")
        print("="*80)
        
        try:
            # Get available books
            available_books = self.book_service.get_available_books()
            
            if not available_books:
                print("\n❌ Hiện tại không có sách nào có sẵn để thuê.")
                return
            
            print(f"\n📚 Có {len(available_books)} cuốn sách có sẵn:")
            self._print_available_books_table(available_books)
            
            # Get customer info
            customer = self.customer_service.get_customer_by_id(self.user.customer_id)
            
            print(f"\n👤 Khách hàng: {customer.fullname}")
            print(f"   Mã khách: {customer.customer_code}")
            
            # Select books
            print("\nNhập mã sách muốn thuê (cách nhau bằng dấu phẩy):")
            print("Ví dụ: BOOK01,BOOK02,BOOK03")
            
            book_codes_str = input("\nDanh sách mã sách: ").strip()
            book_codes = [code.strip() for code in book_codes_str.split(",") if code.strip()]
            
            if not book_codes:
                print("❌ Phải chọn ít nhất một cuốn sách.")
                return
            
            # Validate book codes
            invalid_codes = []
            for code in book_codes:
                try:
                    book = self.book_service.get_book_by_code(code)
                    if book.book_status != 'Available':
                        invalid_codes.append(f"{code} (không có sẵn)")
                except BookNotFoundError:
                    invalid_codes.append(f"{code} (không tồn tại)")
            
            if invalid_codes:
                print("\n❌ Lỗi: Một số sách không hợp lệ:")
                for invalid in invalid_codes:
                    print(f"   - {invalid}")
                return
            
            # Show selected books
            print("\n✅ Sách bạn chọn thuê:")
            for i, code in enumerate(book_codes, 1):
                book = self.book_service.get_book_by_code(code)
                print(f"   {i}. {book.book_code} - {book.title} ({book.author})")
            
            # Get return date
            print("\n📅 Nhập ngày dự kiến trả sách:")
            date_str = input("Ngày trả (DD/MM/YYYY): ").strip()
            
            try:
                expected_return_date = datetime.strptime(date_str, "%d/%m/%Y")
            except ValueError:
                print("❌ Định dạng ngày không hợp lệ. Vui lòng nhập theo DD/MM/YYYY")
                return
            
            # Validate return date
            if expected_return_date < datetime.now():
                print("❌ Ngày trả phải lớn hơn hoặc bằng hôm nay.")
                return
            
            # Confirm rental
            print("\n📋 Xác nhận thông tin thuê sách:")
            print(f"   Khách hàng: {customer.fullname}")
            print(f"   Số sách: {len(book_codes)}")
            print(f"   Ngày trả dự kiến: {expected_return_date.strftime('%d/%m/%Y')}")
            
            confirm = input("\nBạn chắc chắn muốn thuê sách này? (yes/no): ").strip().lower()
            
            if confirm != 'yes':
                print("❌ Thuê sách bị hủy.")
                return
            
            # Create order
            order_id = self.order_service.create_rental_order(
                customer_id=self.user.customer_id,
                book_codes=book_codes,
                expected_return_date=expected_return_date
            )
            
            order = self.order_service.get_order_by_id(order_id)
            
            print(f"\n✅ Thuê sách thành công!")
            print(f"   Mã đơn thuê: {order.order_code}")
            print(f"   Ngày thuê: {order.rent_date.strftime('%d/%m/%Y')}")
            print(f"   Ngày trả dự kiến: {order.expected_return_date.strftime('%d/%m/%Y')}")
            print(f"   Số sách: {len(book_codes)}")
            print(f"\n📌 Vui lòng đến quầy nhân viên để nhận sách.")
            
        except BookNotAvailableError as e:
            print(f"\n❌ {e.message}")
        except Exception as e:
            print(f"\n❌ Lỗi: {str(e)}")
    
    # ==================== XEM ĐƠN THUÊ ĐANG HOẠT ĐỘNG ====================
    
    def _handle_view_renting_orders(self):
        """View currently renting orders"""
        print("\n" + "="*80)
        print("📤 SÁCH ĐANG THUÊ")
        print("="*80)
        
        try:
            renting_orders = self.order_service.get_customer_renting_orders(self.user.customer_id)
            
            if not renting_orders:
                print("\nBạn hiện không thuê cuốn sách nào.")
                return
            
            print(f"\n✅ Bạn đang thuê {len(renting_orders)} đơn sách:")
            
            for order in renting_orders:
                self._print_order_detail(order)
                
        except Exception as e:
            print(f"\n❌ Lỗi: {str(e)}")
    
    # ==================== XEM LỊCH SỬ ĐƠN THUÊ ====================
    
    def _handle_view_all_orders(self):
        """View all rental orders history"""
        print("\n" + "="*80)
        print("📋 LỊCH SỬ THUÊ SÁCH")
        print("="*80)
        
        try:
            all_orders = self.order_service.get_customer_all_orders(self.user.customer_id)
            
            if not all_orders:
                print("\nBạn chưa thuê cuốn sách nào.")
                return
            
            renting = [o for o in all_orders if o.order_status == 'Renting']
            returned = [o for o in all_orders if o.order_status == 'Returned']
            
            print(f"\n📊 Thống kê:")
            print(f"   Đang thuê: {len(renting)}")
            print(f"   Đã trả: {len(returned)}")
            print(f"   Tổng cộng: {len(all_orders)}")
            
            if renting:
                print(f"\n📤 ĐƠN ĐANG THUÊ ({len(renting)}):")
                for order in renting:
                    self._print_order_summary(order)
            
            if returned:
                print(f"\n✅ ĐƠN ĐÃ TRẢ ({len(returned)}):")
                for order in returned:
                    self._print_order_summary(order)
                
        except Exception as e:
            print(f"\n❌ Lỗi: {str(e)}")
    
    # ==================== HELPER METHODS ====================
    
    def _print_available_books_table(self, books):
        """Print table of available books"""
        print("-" * 100)
        print(f"{'STT':<5} | {'Mã Sách':<12} | {'Tên Sách':<40} | {'Tác Giả':<20} | {'Thể Loại':<15}")
        print("-" * 100)
        
        for i, book in enumerate(books, 1):
            category = book.category or "Chưa xác định"
            print(f"{i:<5} | {book.book_code:<12} | {book.title[:40]:<40} | {book.author[:20]:<20} | {category[:15]:<15}")
    
    def _print_books_table(self, books):
        """Print formatted books table with status"""
        print("-" * 110)
        print(f"{'STT':<5} | {'Mã Sách':<12} | {'Tên Sách':<40} | {'Tác Giả':<20} | {'Trạng Thái':<15}")
        print("-" * 110)
        
        for i, book in enumerate(books, 1):
            status_display = {
                'Available': '✅ Có sẵn',
                'Rented': '📤 Đang thuê',
                'Damaged': '⚠️  Hỏng',
                'Lost': '❌ Mất'
            }.get(book.book_status, book.book_status)
            
            print(f"{i:<5} | {book.book_code:<12} | {book.title[:40]:<40} | {book.author[:20]:<20} | {status_display:<15}")
    
    def _print_order_detail(self, order):
        """Print detailed order information"""
        try:
            details = self.order_service.get_order_details(order.order_id)
            
            print(f"\n📦 Mã đơn: {order.order_code}")
            print(f"   Ngày thuê: {order.rent_date.strftime('%d/%m/%Y')}")
            print(f"   Ngày dự kiến trả: {order.expected_return_date.strftime('%d/%m/%Y')}")
            
            if order.return_date:
                print(f"   Ngày trả thực tế: {order.return_date.strftime('%d/%m/%Y')}")
            
            print(f"\n   📚 Sách trong đơn ({len(details)}):")
            for i, detail in enumerate(details, 1):
                print(f"      {i}. {detail.book_code} - {detail.title}")
                print(f"         Tác giả: {detail.author}")
            
        except Exception as e:
            print(f"   ❌ Lỗi khi lấy thông tin chi tiết: {str(e)}")
    
    def _print_order_summary(self, order):
        """Print order summary"""
        try:
            details = self.order_service.get_order_details(order.order_id)
            status = '📤 Đang thuê' if order.order_status == 'Renting' else '✅ Đã trả'
            
            print(f"\n   Mã đơn: {order.order_code} | {status}")
            print(f"   Ngày thuê: {order.rent_date.strftime('%d/%m/%Y')} | Dự kiến trả: {order.expected_return_date.strftime('%d/%m/%Y')}")
            print(f"   Số sách: {len(details)}", end="")
            
            if details:
                print(f" - {', '.join([d.book_code for d in details[:3]])}{'...' if len(details) > 3 else ''}")
            else:
                print()
            
        except Exception as e:
            print(f"   ❌ Lỗi: {str(e)}")