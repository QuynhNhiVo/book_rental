# 📚 Book Rental Management System - Frontend

## Giới thiệu

Ứng dụng web quản lý tiệm thuê sách được xây dựng bằng **ReactJS** với **Tailwind CSS**, cung cấp giao diện hiện đại, responsive và dễ sử dụng cho cả PC và Tablet.

## ✨ Tính năng chính

### 👨‍💼 Dành cho Admin
- 📊 Dashboard với thống kê toàn bộ hệ thống
- 📚 Quản lý sách (CRUD)
- 👥 Quản lý khách hàng
- 📝 Quản lý đơn thuê
- 📈 Báo cáo & Thống kê

### 👤 Dành cho Khách hàng
- 🔍 Tìm kiếm & duyệt sách
- 📋 Xem đơn thuê của mình
- 📊 Dashboard cá nhân

## 🛠️ Công nghệ sử dụng

| Công nghệ | Phiên bản | Mục đích |
|-----------|---------|---------|
| React | 18.2.0 | Framework chính |
| TypeScript | 5.3.0 | Type safety |
| Tailwind CSS | 3.3.6 | Styling |
| Vite | 5.0.0 | Build tool |
| React Router | 6.20.0 | Routing |
| Lucide React | 0.294.0 | Icons |
| Axios | 1.6.0 | HTTP Client |

## 📁 Cấu trúc thư mục

```
frontend_react/
├── src/
│   ├── components/          # Reusable components
│   │   ├── Sidebar.tsx      # Navigation sidebar
│   │   ├── StatCard.tsx     # Statistics card
│   │   ├── Modal.tsx        # Modal dialog
│   │   └── Table.tsx        # Data table
│   ├── pages/               # Page components
│   │   ├── Login.tsx        # Login page
│   │   ├── Dashboard.tsx    # Dashboard
│   │   ├── Books.tsx        # Books management
│   │   ├── Customers.tsx    # Customers management
│   │   ├── Orders.tsx       # Orders management
│   │   └── Reports.tsx      # Reports & Analytics
│   ├── App.tsx              # Main app component
│   ├── main.tsx             # Entry point
│   └── index.css            # Global styles
├── index.html               # HTML template
├── package.json             # Dependencies
├── tsconfig.json            # TypeScript config
├── vite.config.ts           # Vite config
├── tailwind.config.js       # Tailwind config
└── postcss.config.js        # PostCSS config
```

## 🚀 Hướng dẫn cài đặt và khởi chạy

### Bước 1: Chuẩn bị môi trường

```bash
# Yêu cầu: Node.js >= 16.0.0
node --version
npm --version
```

### Bước 2: Cài đặt dependencies

```bash
cd frontend_react
npm install
```

### Bước 3: Khởi chạy development server

```bash
npm run dev
```

Ứng dụng sẽ chạy tại: **http://localhost:3000**

### Bước 4: Build production

```bash
npm run build
```

Các file build sẽ được tạo trong thư mục `dist/`

### Bước 5: Preview production build

```bash
npm run preview
```

## 🎨 Tùy chỉnh giao diện

### Màu sắc

Tệp `tailwind.config.js` chứa cấu hình màu sắc:

```javascript
theme: {
  extend: {
    colors: {
      primary: {
        50: '#f5f3f0',  // Màu nhạt nhất
        ...
        900: '#1f170a', // Màu tối nhất
      },
      secondary: {
        // Xanh dương series
      },
    },
  },
}
```

**Thay đổi màu sắc:**
- Cập nhật giá trị hex trong `tailwind.config.js`
- Hoặc sử dụng Tailwind color picker

### Font

Mặc định sử dụng font Inter. Để thay đổi:

```css
/* src/index.css */
html {
  font-family: 'Your Font', sans-serif;
}
```

### Responsive Design

Ứng dụng hỗ trợ breakpoints:
- `sm`: 640px (Mobile)
- `md`: 768px (Tablet)
- `lg`: 1024px (Desktop)
- `xl`: 1280px (Large Desktop)

```tsx
// Ví dụ: Ẩn trên mobile, hiển thị trên tablet
<div className="hidden md:block">
  Content chỉ hiển thị trên tablet và lớn hơn
</div>
```

## 🔌 Kết nối API Backend

### Cấu hình API

Sửa file `vite.config.ts`:

```typescript
server: {
  proxy: {
    '/api': {
      target: 'http://localhost:5000',  // URL backend
      changeOrigin: true,
      rewrite: (path) => path.replace(/^\/api/, '/api/v1'),
    },
  },
}
```

### Sử dụng Axios

```typescript
import axios from 'axios'

// GET
const books = await axios.get('/api/books')

// POST
const newBook = await axios.post('/api/books', {
  title: 'Clean Code',
  author: 'Robert Martin'
})

// PUT
await axios.put('/api/books/1', { title: 'Updated Title' })

// DELETE
await axios.delete('/api/books/1')
```

## 📊 Mock Data

Dữ liệu mẫu được lưu trữ trực tiếp trong các component page:

```typescript
const mockBooks = [
  { id: 1, code: 'B001', title: 'Clean Code', ... },
  // ...
]
```

Để kết nối với API thực:

```typescript
useEffect(() => {
  const fetchBooks = async () => {
    const response = await axios.get('/api/books')
    setBooks(response.data.data)
  }
  fetchBooks()
}, [])
```

## 🧩 Thành phần chính

### 1. Sidebar Component

```tsx
<Sidebar userRole="Admin" onLogout={handleLogout} />
```

**Props:**
- `userRole`: 'Admin' | 'Customer'
- `onLogout`: () => void

### 2. StatCard Component

```tsx
<StatCard
  icon={<BookOpen size={24} />}
  label="Tổng sách"
  value={150}
  trend={5}
  color="primary"
/>
```

**Props:**
- `icon`: React.ReactNode
- `label`: string
- `value`: string | number
- `trend`: number (optional)
- `color`: 'primary' | 'secondary' | 'green' | 'orange'

### 3. Modal Component

```tsx
<Modal
  title="Thêm sách mới"
  isOpen={isModalOpen}
  onClose={() => setIsModalOpen(false)}
>
  {/* Form content */}
</Modal>
```

### 4. Table Component

```tsx
<Table
  columns={[
    { key: 'code', label: 'Mã sách' },
    { key: 'title', label: 'Tiêu đề' },
  ]}
  data={books}
  actions={(row) => <button>Edit</button>}
/>
```

## 🎯 Hướng dẫn sử dụng

### Đăng nhập

1. Vào trang login: http://localhost:3000
2. Nhập credentials demo:
   - Username: `admin`
   - Password: `password`
3. Chọn vai trò (Admin hoặc Customer)
4. Nhấn "Đăng nhập"

### Quản lý sách

**Xem danh sách:**
- Vào mục "Sách" trong sidebar
- Tìm kiếm bằng ô search

**Thêm sách:**
- Nhấn nút "+ Thêm sách"
- Điền thông tin
- Nhấn "Lưu"

**Chỉnh sửa:**
- Nhấn icon ✏️ trên hàng cần chỉnh
- Cập nhật thông tin
- Nhấn "Lưu"

**Xóa:**
- Nhấn icon 🗑️ trên hàng
- Xác nhận xóa

### Tạo đơn thuê

1. Vào mục "Đơn thuê"
2. Nhấn "+ Tạo đơn mới"
3. Chọn khách hàng
4. Chọn sách cần thuê
5. Chọn ngày trả
6. Nhấn "Lưu"

## 🔐 Bảo mật

### Xác thực

Thêm token JWT vào header của mỗi request:

```typescript
axios.interceptors.request.use((config) => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})
```

### Lưu trữ token

```typescript
// Lưu token sau khi login
localStorage.setItem('token', response.data.token)

// Lấy token khi cần
const token = localStorage.getItem('token')

// Xóa token khi logout
localStorage.removeItem('token')
```

## 🐛 Debugging

### React Developer Tools

Cài đặt extension React Developer Tools để debug component:

```bash
# Chrome: React Developer Tools
# Firefox: React Developer Tools
```

### Console Logs

```typescript
console.log('Giá trị:', value)
console.error('Lỗi:', error)
console.table(arrayData) // Hiển thị dữ liệu dạng bảng
```

### Network Tab

Sử dụng DevTools > Network tab để kiểm tra:
- Request/Response API
- Status code
- Headers

## 📱 Responsive Testing

```bash
# Mở DevTools: F12 hoặc Ctrl+Shift+I
# Bật Device Mode: Ctrl+Shift+M
# Chọn thiết bị: iPhone, iPad, Galaxy, etc.
```

## 🚀 Deployment

### Vercel (Recommended)

```bash
# Cài đặt Vercel CLI
npm install -g vercel

# Deploy
vercel
```

### Netlify

```bash
# Cài đặt Netlify CLI
npm install -g netlify-cli

# Deploy
netlify deploy --prod --dir=dist
```

### GitHub Pages

```bash
# Cập nhật vite.config.ts
base: '/book-rental/',

# Build
npm run build

# Deploy (push dist folder to gh-pages branch)
```

## 📚 Tài liệu tham khảo

- [React Documentation](https://react.dev)
- [TypeScript Handbook](https://www.typescriptlang.org/docs)
- [Tailwind CSS Docs](https://tailwindcss.com/docs)
- [Vite Documentation](https://vitejs.dev)
- [React Router](https://reactrouter.com)
- [Lucide Icons](https://lucide.dev)

## ❓ Troubleshooting

### Port 3000 đã được sử dụng

```bash
# Chỉ định port khác
npm run dev -- --port 3001
```

### Build fail

```bash
# Xóa node_modules và cài lại
rm -rf node_modules package-lock.json
npm install
npm run build
```

### API không kết nối

1. Kiểm tra backend đang chạy: http://localhost:5000
2. Kiểm tra proxy config trong vite.config.ts
3. Kiểm tra CORS settings trên backend

## 📞 Hỗ trợ

Nếu gặp vấn đề, hãy:

1. Kiểm tra console (F12)
2. Xem lại file cấu hình
3. Thử xóa node_modules và cài lại
4. Kiểm tra version Node.js

---

