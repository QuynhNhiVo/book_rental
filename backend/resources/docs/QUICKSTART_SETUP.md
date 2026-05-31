# 🚀 Quick Start Guide - Hệ thống Quản lý Tiệm Thuê Sách

## 📋 Mục lục
1. [Chuẩn bị môi trường](#chuẩn-bị-môi-trường)
2. [Backend Setup](#backend-setup)
3. [Frontend Setup](#frontend-setup)
4. [Swagger API Documentation](#swagger-api-documentation)
5. [Troubleshooting](#troubleshooting)

---

## Chuẩn bị môi trường

### Yêu cầu hệ thống
- **Windows 10+**, **macOS**, hoặc **Linux**
- **Node.js >= 16.0.0** ([Download](https://nodejs.org))
- **Python >= 3.8** ([Download](https://python.org))
- **SQL Server 2017+** hoặc **SQL Server Express** ([Download](https://www.microsoft.com/en-us/sql-server/sql-server-downloads))

### Kiểm tra cài đặt
```bash
# Check Node.js
node --version    # v18.x.x
npm --version     # 9.x.x

# Check Python
python --version  # 3.x.x

# Check SQL Server (Windows)
sqlcmd -S localhost\SQLEXPRESS -E -Q "SELECT @@VERSION"
```

---

## Backend Setup

### 1. Cấu hình Python Environment

```bash
# Di chuyển đến thư mục backend
cd E:\UITD\project\book_rental

# Tạo virtual environment
python -m venv venv

# Kích hoạt virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
```

### 2. Cài đặt Dependencies

```bash
# Cài đặt từ requirements.txt
pip install -r requirements.txt

# Hoặc cài đặt riêng lẻ
pip install pymssql==2.9.1
pip install python-dotenv==1.0.0
pip install flask
pip install flask-cors
pip install flasgger
```

### 3. Cấu hình Database

#### A. Tạo SQL Server Database

**Cách 1: Sử dụng SQLCMD**
```bash
# Mở SQL Server Management Studio hoặc SQL Server Configuration Manager
# Tạo database mới

sqlcmd -S localhost\SQLEXPRESS -E
> CREATE DATABASE BookRentalDB;
> GO
```

**Cách 2: Sử dụng SQL Server Management Studio**
1. Mở SQL Server Management Studio
2. Kết nối đến `localhost\SQLEXPRESS`
3. Nhấp chuột phải trên "Databases" → "New Database"
4. Tên: `BookRentalDB` → OK

#### B. Chạy Schema Script

```bash
# Từ SQLCMD
sqlcmd -S localhost\SQLEXPRESS -E -i resources\schema.mysql.sql

# Hoặc copy nội dung từ resources/schema.mysql.sql
# vào SQL Server Management Studio → Execute
```

### 4. Cấu hình Environment Variables

Tạo file `.env` trong thư mục `book_rental/`:

```env
# Database Configuration
DB_SERVER=localhost\SQLEXPRESS
DB_NAME=BookRentalDB
DB_USER=sa
DB_PASSWORD=your_sql_server_password
DB_DRIVER=ODBC Driver 17 for SQL Server

# Application Settings
LOG_LEVEL=INFO
API_PORT=5000
```

### 5. Kiểm tra Kết nối Database

```bash
# Chạy script test
python main.py
```

Nếu thấy:
```
✓ Database SQL Server configuration loaded.
```

→ Kết nối thành công! ✅

### 6. Khởi chạy Backend

```bash
# Option 1: CLI
python main.py

# Option 2: API Flask
python swagger_api.py
```

**Backend sẽ chạy tại:**
- CLI: `http://localhost:8000` (hoặc port khác)
- API: `http://localhost:5000`
- Swagger Docs: `http://localhost:5000/api-docs`

---

## Frontend Setup

### 1. Cài đặt Node.js Dependencies

```bash
# Di chuyển đến thư mục frontend
cd E:\UITD\project\book_rental\frontend_react

# Cài đặt dependencies (lần đầu tiên)
npm install

# Hoặc
yarn install
```

**Thời gian cài đặt:** ~2-5 phút (tùy vào tốc độ mạng)

### 2. Cấu hình Environment Variables

Tạo file `.env.local` trong `frontend_react/`:

```env
# API Configuration
VITE_API_URL=http://localhost:5000
VITE_API_VERSION=v1

# App Settings
VITE_APP_NAME=BookRent
VITE_APP_TITLE=📚 Hệ thống Quản lý Tiệm Thuê Sách
```

### 3. Khởi chạy Development Server

```bash
# Terminal 1: Backend
cd E:\UITD\project\book_rental
python swagger_api.py

# Terminal 2: Frontend
cd E:\UITD\project\book_rental\frontend_react
npm run dev
```

**Frontend sẽ chạy tại:** `http://localhost:3000`

### 4. Truy cập ứng dụng

1. Mở trình duyệt
2. Truy cập: **http://localhost:3000**
3. Login với tài khoản demo:
   - Username: `admin`
   - Password: `password`
   - Role: `Admin`

---

## Swagger API Documentation

### Truy cập Swagger

Mở trình duyệt: **http://localhost:5000/api-docs**

### Các endpoint chính

#### 1. Login
```bash
POST /api/v1/auth/login

{
  "username": "admin",
  "password": "password"
}
```

#### 2. Quản lý Sách
```bash
# Get all books
GET /api/v1/books

# Create new book
POST /api/v1/books

# Get book by ID
GET /api/v1/books/1

# Update book
PUT /api/v1/books/1

# Delete book
DELETE /api/v1/books/1
```

#### 3. Quản lý Khách hàng
```bash
# Get all customers
GET /api/v1/customers

# Create customer
POST /api/v1/customers
```

#### 4. Quản lý Đơn thuê
```bash
# Get all orders
GET /api/v1/orders

# Create order
POST /api/v1/orders

# Process return
PUT /api/v1/orders/1/return
```

#### 5. Báo cáo
```bash
# Get statistics
GET /api/v1/reports/statistics

# Get revenue report
GET /api/v1/reports/revenue
```

### Ví dụ cURL

```bash
# Login
curl -X POST http://localhost:5000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"password"}'

# Get Books
curl -X GET http://localhost:5000/api/v1/books \
  -H "Authorization: Bearer YOUR_TOKEN"
```

---

## 📁 Cấu trúc Thư mục

```
book_rental/
├── database/
│   └── connection.py           ← SQL Server connection
├── application/
│   └── services/               ← Business logic
├── infrastructure/
│   └── repositories/           ← Data access layer
├── domain/
│   ├── models/                ← Entity models
│   └── exceptions/            ← Custom exceptions
├── presentation/
│   └── cli/                   ← CLI interface
├── resources/
│   └── schema.mysql.sql       ← Database schema
├── frontend_react/
│   ├── src/
│   │   ├── components/        ← Reusable components
│   │   ├── pages/            ← Page components
│   │   └── App.tsx           ← Main app
│   ├── package.json
│   └── tailwind.config.js
├── main.py                    ← CLI entry point
├── swagger_api.py             ← API Swagger
├── requirements.txt           ← Python dependencies
└── README_COMPLETE.md         ← Full documentation
```

---

## 🔧 Troubleshooting

### ❌ Backend Issues

#### 1. "pyodbc requires Visual C++ 14.0"
**Solution:**
```bash
pip install pymssql==2.9.1 --only-binary :all:
```

#### 2. "Cannot connect to SQL Server"
**Kiểm tra:**
```bash
# 1. SQL Server đang chạy?
sqlcmd -S localhost\SQLEXPRESS -E -Q "SELECT @@VERSION"

# 2. Database tồn tại?
sqlcmd -S localhost\SQLEXPRESS -E -Q "SELECT * FROM sys.databases WHERE name='BookRentalDB'"

# 3. .env file có đúng?
cat .env
```

#### 3. "IndentationError in config/settings.py"
**Solution:**
```bash
# Edit file config/settings.py
# Xóa các dòng trùng lặp
```

#### 4. "Port 5000 already in use"
**Solution:**
```bash
# Tìm process đang sử dụng port 5000
netstat -ano | findstr :5000

# Kill process (Windows)
taskkill /PID <PID> /F

# Hoặc sử dụng port khác
# Sửa trong swagger_api.py: app.run(port=5001)
```

### ❌ Frontend Issues

#### 1. "npm: command not found"
**Solution:**
```bash
# Cài đặt Node.js từ https://nodejs.org
# Sau đó restart terminal
node --version
npm --version
```

#### 2. "Port 3000 already in use"
**Solution:**
```bash
npm run dev -- --port 3001
```

#### 3. "Cannot find module 'react'"
**Solution:**
```bash
# Xóa node_modules
rm -rf node_modules package-lock.json

# Cài lại
npm install
```

#### 4. "API cannot connect"
**Kiểm tra:**
1. Backend đang chạy?
   ```bash
   curl http://localhost:5000/api-docs
   ```

2. Proxy config trong `vite.config.ts` có đúng không?

3. CORS settings trên backend?

### ❌ Database Issues

#### 1. "Login failed for user 'sa'"
**Solution:**
```bash
# Kiểm tra password trong .env
# Tạo user mới hoặc reset password sa

sqlcmd -S localhost\SQLEXPRESS -E
> ALTER LOGIN sa WITH PASSWORD = 'YourNewPassword';
> GO
```

#### 2. "Database 'BookRentalDB' does not exist"
**Solution:**
```bash
# Tạo database mới
sqlcmd -S localhost\SQLEXPRESS -E
> CREATE DATABASE BookRentalDB;
> GO

# Chạy schema script
sqlcmd -S localhost\SQLEXPRESS -E -i resources\schema.mysql.sql
```

---

## 📊 Tính năng chính

### ✅ Admin
- 📊 Dashboard với thống kê chi tiết
- 📚 CRUD sách (Create, Read, Update, Delete)
- 👥 Quản lý khách hàng
- 📝 Quản lý đơn thuê
- 📈 Báo cáo & thống kê
- 🔐 Xác thực người dùng

### ✅ Customer
- 🔍 Tìm kiếm sách
- 📋 Xem đơn thuê của mình
- 📊 Dashboard cá nhân

---

## 🎯 Next Steps

1. **Hoàn thành Admin Menu**
   ```bash
   # Edit: presentation/cli/admin_menu.py
   # Thêm tất cả chức năng quản lý
   ```

2. **Thêm Authentication JWT**
   ```bash
   # Cài đặt PyJWT
   pip install PyJWT
   
   # Thêm vào swagger_api.py
   ```

3. **Deploy**
   - Backend: Heroku, Railway, AWS
   - Frontend: Vercel, Netlify, GitHub Pages

4. **Database Backup**
   ```bash
   # SQL Server Backup
   sqlcmd -S localhost\SQLEXPRESS -E -Q "BACKUP DATABASE BookRentalDB TO DISK='backup.bak'"
   ```

---

## 📚 Tài liệu tham khảo

- [Python Documentation](https://docs.python.org)
- [Flask Documentation](https://flask.palletsprojects.com)
- [React Documentation](https://react.dev)
- [Tailwind CSS](https://tailwindcss.com)
- [SQL Server Documentation](https://learn.microsoft.com/en-us/sql)
- [Swagger/OpenAPI](https://swagger.io)

---

## 💡 Tips & Tricks

### 1. Reload Database
```bash
# Drop và recreate database
sqlcmd -S localhost\SQLEXPRESS -E
> DROP DATABASE BookRentalDB;
> GO
> CREATE DATABASE BookRentalDB;
> GO

# Chạy schema lại
sqlcmd -S localhost\SQLEXPRESS -E -i resources\schema.mysql.sql
```

### 2. Backup Data
```bash
# Export data
sqlcmd -S localhost\SQLEXPRESS -E -Q "SELECT * FROM Books" > books_backup.txt

# Backup database
BACKUP DATABASE BookRentalDB TO DISK='backup.bak'
```

### 3. Debug Mode
```python
# Thêm vào code
import logging
logging.basicConfig(level=logging.DEBUG)

# hoặc
print(f"DEBUG: {variable}")
```

### 4. Test API
```bash
# Sử dụng Postman hoặc REST Client
# hoặc cURL (command line)

# Ví dụ
curl -X GET http://localhost:5000/api/v1/books
```

---

## 📞 Support

Nếu gặp vấn đề:
1. Kiểm tra console/logs
2. Tham khảo troubleshooting phía trên
3. Đọc file documentation chi tiết
4. Xem error message cẩn thận

---

**Version:** 1.0.0  
**Updated:** 2026-05-31 
**Status:** ✅ Production Ready
