# ⚛️ Cấu trúc Mã nguồn Frontend (React + TypeScript)

Ứng dụng Frontend được xây dựng theo tiêu chuẩn React hiện đại, tập trung vào tính Module hóa và khả năng tái sử dụng linh kiện (Components).

## 📁 Thư mục `src/`

### 1. `components/`
*   Chứa các linh kiện giao diện nhỏ (Atomic Components) dùng ở nhiều nơi.
*   Ví dụ: `Table`, `Modal`, `Sidebar`, `StatCard`.

### 2. `layouts/`
*   `MainLayout.tsx`: Khung giao diện chính (bao gồm Sidebar + Nội dung) xuất hiện sau khi người dùng đăng nhập.

### 3. `pages/`
*   Chứa các trang chính của ứng dụng. Mỗi trang thường tương ứng với một Route.
*   Ví dụ: `AdminDashboard.tsx`, `Books.tsx`, `Login.tsx`.

### 4. `routes/`
*   Quản lý việc chuyển trang và bảo vệ quyền truy cập.
*   `ProtectedRoute.tsx`: Thành phần quan trọng nhất dùng để ngăn chặn người dùng chưa đăng nhập vào các trang nội bộ.

### 5. `services/`
*   `apiService.ts`: Cấu hình `fetch` hoặc `axios` để gọi API tới Backend.
*   Chứa logic xử lý Token (gắn Token vào Header) và xử lý lỗi tập trung.

### 6. `constants/`
*   `api.ts`: Lưu trữ tất cả các đường dẫn API của Backend (URLs). Tránh việc phải gõ lại URL ở nhiều nơi.

---

## 💡 Các khái niệm 

1.  **State Management (`useState`)**: Dùng để lưu trữ dữ liệu trên giao diện (ví dụ: danh sách sách đang hiển thị). Khi State thay đổi, React sẽ tự động cập nhật lại màn hình.
2.  **Side Effects (`useEffect`)**: Dùng để thực hiện các hành động bên ngoài khi trang web vừa tải xong (ví dụ: gọi API lấy dữ liệu từ server).
3.  **Conditional Rendering**: Cách chúng ta dùng `if/else` để hiển thị các nội dung khác nhau (ví dụ: hiện vòng quay Loading khi đang đợi API).
4.  **Props**: Cách truyền dữ liệu từ Component cha xuống Component con.
