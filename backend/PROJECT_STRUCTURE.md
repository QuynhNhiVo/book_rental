# 🏗️ Cấu trúc Mã nguồn Backend (Layered/MVC)

Hệ thống Backend được thiết kế theo mô hình phân lớp, giúp tách biệt trách nhiệm giữa việc quản lý dữ liệu, nghiệp vụ logic và giao diện API.

## 📁 Thư mục `src/`

### 1. `configs/`
*   **Mục đích**: Lưu trữ mọi cấu hình của ứng dụng.
*   `settings.py`: Đọc biến môi trường từ `.env` (DB Host, Port, Secret Key...).
*   `database.py`: Quản lý kết nối SQL Server và cung cấp các hàm thực thi query dùng chung.

### 2. `models/`
*   **Mục đích**: Định nghĩa cấu trúc dữ liệu cho các đối tượng trong hệ thống (Book, User, Customer, Order).
*   Sử dụng Python `dataclass` để code ngắn gọn, súc tích.

### 3. `repositories/`
*   **Mục đích**: Lớp truy vấn dữ liệu trực tiếp từ Database.
*   Chỉ chứa các câu lệnh SQL. Không chứa logic nghiệp vụ (ví dụ: không kiểm tra sách có sẵn hay không ở đây).

### 4. `services/`
*   **Mục đích**: **Trái tim của ứng dụng**. Chứa toàn bộ Logic nghiệp vụ.
*   Ví dụ: Khi khách hàng thuê sách, Service sẽ kiểm tra: Khách có tồn tại không? Sách có đang rảnh không? Ngày trả có hợp lệ không? Nếu ok mới gọi sang Repository để lưu.

### 5. `controllers/`
*   **Mục đích**: Tiếp nhận Request từ người dùng, gọi xuống Service tương ứng và trả về Response (JSON).
*   Giúp giữ cho mã nguồn API gọn gàng, không bị lẫn lộn logic tính toán.

### 6. `routes/`
*   **Mục đích**: Định nghĩa các đường dẫn API (URL).
*   Sử dụng Flask `Blueprint` để nhóm các API liên quan (Auth, Admin, User).

### 7. `middlewares/`
*   **Mục đích**: Các lớp xử lý trung gian.
*   `auth_middleware.py`: Kiểm tra xem Token gửi lên có hợp lệ không, người dùng có quyền Admin hay không trước khi cho phép vào Controller.

---

## 🔄 Luồng chạy của một Request (Dành cho người mới học)

Khi bạn click nút "Thuê sách" trên UI:
1.  **Route**: Nhận URL `/api/v1/user/rentals/create`.
2.  **Middleware**: Kiểm tra bạn đã đăng nhập chưa.
3.  **Controller**: Bóc tách dữ liệu JSON từ request.
4.  **Service**: Kiểm tra sách đó có ai thuê chưa (Logic nghiệp vụ).
5.  **Repository**: Nếu mọi thứ ổn, ghi vào bảng `RentalOrders` trong DB.
6.  **Response**: Trả về thông báo "Thành công" cho Frontend.
