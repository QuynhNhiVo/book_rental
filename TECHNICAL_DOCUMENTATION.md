# TÀI LIỆU KỸ THUẬT DỰ ÁN: HỆ THỐNG QUẢN LÝ THUÊ SÁCH

## 1. Giới thiệu Dự án
Hệ thống Quản lý Thuê sách là một giải pháp chuyển đổi số cho các thư viện và cửa hàng thuê sách truyền thống. Mục tiêu của dự án là tối ưu hóa quy trình quản lý kho, theo dõi đơn thuê và cung cấp nền tảng đăng ký trực tuyến thuận tiện cho khách hàng.

## 2. Công nghệ và Lý do lựa chọn (Tech Stack Selection)

### 2.1 Backend: Flask (Python)
*   **Lý do**: Flask là một Micro-framework linh hoạt, dễ học và triển khai nhanh. Python có hệ sinh thái thư viện xử lý dữ liệu mạnh mẽ, phù hợp cho việc mở rộng tính năng báo cáo sau này.
*   **Xác thực**: Sử dụng JWT (JSON Web Token) để đảm bảo tính stateless và bảo mật cho API.

### 2.2 Frontend: React (Vite + TypeScript)
*   **Lý do**: React giúp xây dựng giao diện người dùng (UI) có tính tương tác cao. TypeScript giúp kiểm soát kiểu dữ liệu chặt chẽ, giảm thiểu lỗi runtime trong quá trình phát triển.
*   **Styling**: Tailwind CSS giúp thiết kế giao diện hiện đại, responsive một cách nhanh chóng.

### 2.3 Database: SQL Server (MSSQL)
*   **Lý do**: Phổ biến trong môi trường doanh nghiệp và đào tạo CNTT tại Việt Nam, hỗ trợ tốt các giao dịch (Transactions) phức tạp trong quản lý đơn hàng.

## 3. Kiến trúc Hệ thống
Dự án áp dụng mô hình **Layered Architecture (Kiến trúc phân lớp)**:
1.  **Presentation Layer (Flask Controllers)**: Nhận request và trả về JSON.
2.  **Business Logic Layer (Services)**: Xử lý quy tắc nghiệp vụ (Kiểm tra điều kiện thuê sách, tính toán thống kê).
3.  **Data Access Layer (Repositories)**: Thực hiện các câu lệnh SQL tối ưu.
4.  **Database Layer**: Lưu trữ dữ liệu vật lý.

## 4. Thiết kế Cơ sở dữ liệu (Database Schema)
*   `Users`: Lưu thông tin tài khoản và phân quyền (Admin/Customer).
*   `Customers`: Thông tin chi tiết khách hàng (Họ tên, SĐT, Địa chỉ).
*   `Books`: Kho sách (Mã sách, Tên sách, Tác giả, Trạng thái: Có sẵn/Đã thuê).
*   `RentalOrders`: Quản lý thông tin đơn thuê (Ngày thuê, Ngày trả dự kiến).
*   `RentalOrderDetails`: Bảng trung gian quản lý danh sách sách trong mỗi đơn thuê.

## 5. Các Chức năng chính
*   **Hệ thống RBAC**: Tự động chuyển hướng người dùng dựa trên vai trò sau khi đăng nhập thành công.
*   **Quản lý Sách**: Admin có toàn quyền quản lý kho sách. Khách hàng chỉ có quyền xem và tìm kiếm.
*   **Luồng Thuê - Trả**: Quy trình khép kín từ lúc khách hàng tạo đơn -> Sách chuyển trạng thái 'Rented' -> Admin duyệt trả -> Sách quay về trạng thái 'Available'.
*   **Thống kê thời gian thực**: Dashboard cập nhật số liệu ngay khi có giao dịch phát sinh.

## 6. Hướng phát triển
*   **Phí phạt trễ hạn**: Tự động tính toán tiền phạt nếu khách hàng trả sách sau ngày dự kiến.
*   **Tích hợp QR Code**: In mã QR cho từng cuốn sách để quét khi thực hiện giao dịch trả sách nhanh.
*   **Gửi Email thông báo**: Tự động gửi email nhắc nhở khi sắp đến hạn trả sách.

---

