# 📚 Book Rental Management System (RBAC)

Dự án Quản lý Tiệm Thuê Sách chuyên nghiệp, sử dụng kiến trúc phân lớp (Layered Architecture) cho Backend và React cho Frontend.

## 🚀 Tính năng chính

### 🛡️ Phân quyền người dùng (RBAC)
*   **Admin (Quản trị viên)**:
    *   Quản lý kho sách (Thêm, Sửa, Xóa, Liệt kê).
    *   Quản lý danh sách khách hàng.
    *   Quản lý và xử lý đơn thuê sách (Duyệt trả sách).
    *   Xem báo cáo thống kê doanh thu và hoạt động.
*   **Customer (Khách hàng)**:
    *   Xem danh mục sách hiện có.
    *   Đăng ký thuê sách trực tuyến.
    *   Xem lịch sử thuê và các sách đang thuê hiện tại.
    *   Dashboard cá nhân hiển thị thống kê riêng.

## 🛠️ Công nghệ sử dụng

*   **Backend**: Python (Flask), SQL Server (MSSQL), PyJWT, Flasgger (Swagger UI).
*   **Frontend**: React (TypeScript), Tailwind CSS, Lucide Icons, Vite.
*   **Database**: SQL Server.

## 📁 Cấu trúc dự án

*   `/backend`: Chứa mã nguồn server Flask.
*   `/frontend_react`: Chứa mã nguồn giao diện React.
*   `/plans`: Chứa kế hoạch phát triển dự án.

## ⏱️ Khởi chạy nhanh

### 1. Cấu hình Database
*   Cài đặt SQL Server.
*   Chạy script `backend/resources/schema.mysql.sql` để tạo bảng và dữ liệu mẫu.

### 2. Chạy Backend
```bash
cd backend
# Tạo file .env từ .env.example và điền thông tin DB
python run.py
```

### 3. Chạy Frontend
```bash
cd frontend_react
npm install
npm run dev
```

## 📘 Tài liệu hỗ trợ (Dành cho người mới)

Chúng tôi đã chuẩn bị bộ tài liệu chi tiết để bạn dễ dàng tiếp cận:
*   [Kiến trúc Backend](./backend/PROJECT_STRUCTURE.md)
*   [Kiến trúc Frontend](./frontend_react/PROJECT_STRUCTURE.md)
*   [Tài liệu Kỹ thuật chi tiết (Báo cáo đồ án)](./TECHNICAL_DOCUMENTATION.md)
*   [Hướng dẫn API (Swagger)](http://localhost:5000/api-docs) (Khi server đang chạy)

---
