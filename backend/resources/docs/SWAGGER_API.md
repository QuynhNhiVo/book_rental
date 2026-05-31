# 🔌 Swagger API Documentation

## Giới thiệu

Tài liệu API Swagger cho hệ thống quản lý tiệm thuê sách. Tất cả các endpoint đều được xác thực thông qua JWT Bearer Token.

## Truy cập Swagger UI

- **Local:** http://localhost:5000/api-docs
- **URL Schema:** http://localhost:5000/apispec.json

## 🔐 Xác thực

### JWT Authentication

Tất cả các endpoint (ngoại trừ `/auth/login`) yêu cầu token JWT trong header:

```bash
Authorization: Bearer <your_jwt_token>
```

### Ví dụ Header

```json
{
  "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "Content-Type": "application/json"
}
```

## 📚 API Endpoints

### 🔐 Authentication API

#### 1. Login
```http
POST /api/v1/auth/login
Content-Type: application/json

{
  "username": "admin",
  "password": "password123"
}
```

**Response (200):**
```json
{
  "success": true,
  "message": "Login successful",
  "data": {
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "user_id": 1,
    "username": "admin",
    "role": "Admin"
  }
}
```

**Errors:**
- **401:** Invalid credentials
- **400:** Missing required fields

---

### 📚 Books API

#### 2. Get All Books
```http
GET /api/v1/books?status=Available&category=Programming
Authorization: Bearer <token>
```

**Query Parameters:**
- `status` (optional): Available, Rented, Damaged
- `category` (optional): Programming, Fiction, etc.

**Response (200):**
```json
{
  "success": true,
  "data": [
    {
      "book_id": 1,
      "book_code": "B001",
      "title": "Clean Code",
      "author": "Robert C. Martin",
      "category": "Programming",
      "publisher": "Prentice Hall",
      "publish_year": 2008,
      "book_status": "Available"
    }
  ]
}
```

#### 3. Get Book by ID
```http
GET /api/v1/books/{book_id}
Authorization: Bearer <token>
```

**Response (200):**
```json
{
  "success": true,
  "data": {
    "book_id": 1,
    "book_code": "B001",
    "title": "Clean Code",
    "author": "Robert C. Martin",
    "category": "Programming",
    "publisher": "Prentice Hall",
    "publish_year": 2008,
    "book_status": "Available",
    "created_at": "2024-01-15T10:30:00Z",
    "updated_at": "2024-01-20T14:45:00Z"
  }
}
```

**Errors:**
- **404:** Book not found
- **401:** Unauthorized

#### 4. Create Book
```http
POST /api/v1/books
Authorization: Bearer <token>
Content-Type: application/json

{
  "book_code": "B101",
  "title": "The Pragmatic Programmer",
  "author": "David Thomas",
  "category": "Programming",
  "publisher": "Addison-Wesley",
  "publish_year": 2019
}
```

**Response (201):**
```json
{
  "success": true,
  "message": "Book created successfully",
  "data": {
    "book_id": 151,
    "book_code": "B101"
  }
}
```

**Errors:**
- **400:** Invalid input
- **409:** Duplicate book code
- **401:** Unauthorized
- **403:** Insufficient permissions

#### 5. Update Book
```http
PUT /api/v1/books/{book_id}
Authorization: Bearer <token>
Content-Type: application/json

{
  "title": "Clean Code (Revised)",
  "book_status": "Available"
}
```

**Response (200):**
```json
{
  "success": true,
  "message": "Book updated successfully"
}
```

#### 6. Delete Book
```http
DELETE /api/v1/books/{book_id}
Authorization: Bearer <token>
```

**Response (200):**
```json
{
  "success": true,
  "message": "Book deleted successfully"
}
```

**Errors:**
- **404:** Book not found
- **409:** Cannot delete book with active rentals

---

### 👥 Customers API

#### 7. Get All Customers
```http
GET /api/v1/customers?page=1&limit=20
Authorization: Bearer <token>
```

**Query Parameters:**
- `page` (optional): Page number (default: 1)
- `limit` (optional): Records per page (default: 20)

**Response (200):**
```json
{
  "success": true,
  "data": [
    {
      "customer_id": 1,
      "customer_code": "C001",
      "full_name": "Nguyễn Văn A",
      "phone": "0912345678",
      "address": "123 Nguyễn Huệ, HCM",
      "email": "nguyenvana@email.com",
      "created_at": "2024-01-10T08:00:00Z",
      "updated_at": "2024-01-20T10:15:00Z"
    }
  ],
  "pagination": {
    "current_page": 1,
    "total_pages": 5,
    "total_records": 120
  }
}
```

#### 8. Create Customer
```http
POST /api/v1/customers
Authorization: Bearer <token>
Content-Type: application/json

{
  "customer_code": "C121",
  "full_name": "Trần Thị C",
  "phone": "0987654321",
  "address": "456 Lê Lợi, HCM",
  "email": "tranthic@email.com"
}
```

**Response (201):**
```json
{
  "success": true,
  "message": "Customer created successfully",
  "data": {
    "customer_id": 121,
    "customer_code": "C121"
  }
}
```

#### 9. Update Customer
```http
PUT /api/v1/customers/{customer_id}
Authorization: Bearer <token>
Content-Type: application/json

{
  "phone": "0988888888",
  "address": "789 Nguyễn Hữu Cảnh, HCM"
}
```

#### 10. Delete Customer
```http
DELETE /api/v1/customers/{customer_id}
Authorization: Bearer <token>
```

**Errors:**
- **409:** Cannot delete customer with active rentals

---

### 📦 Rental Orders API

#### 11. Get All Orders
```http
GET /api/v1/orders?status=Renting&customer_id=1
Authorization: Bearer <token>
```

**Query Parameters:**
- `status` (optional): Renting, Returned, Overdue
- `customer_id` (optional): Filter by customer
- `page` (optional): Page number
- `limit` (optional): Records per page

**Response (200):**
```json
{
  "success": true,
  "data": [
    {
      "order_id": 1,
      "order_code": "ORD001",
      "customer_id": 1,
      "customer_name": "Nguyễn Văn A",
      "rent_date": "2024-01-15",
      "expected_return_date": "2024-01-25",
      "return_date": null,
      "order_status": "Renting",
      "books_count": 3,
      "created_at": "2024-01-15T10:30:00Z"
    }
  ]
}
```

#### 12. Create Rental Order
```http
POST /api/v1/orders
Authorization: Bearer <token>
Content-Type: application/json

{
  "customer_id": 1,
  "book_ids": [1, 3, 5],
  "rent_date": "2024-01-20",
  "expected_return_date": "2024-02-03"
}
```

**Response (201):**
```json
{
  "success": true,
  "message": "Order created successfully",
  "data": {
    "order_id": 45,
    "order_code": "ORD045"
  }
}
```

**Validation Errors:**
- **400:** Missing required fields
- **409:** Books not available for rental
- **404:** Customer not found

#### 13. Get Order Details
```http
GET /api/v1/orders/{order_id}
Authorization: Bearer <token>
```

**Response (200):**
```json
{
  "success": true,
  "data": {
    "order_id": 1,
    "order_code": "ORD001",
    "customer_id": 1,
    "rent_date": "2024-01-15",
    "expected_return_date": "2024-01-25",
    "return_date": null,
    "order_status": "Renting",
    "books": [
      {
        "book_id": 1,
        "book_code": "B001",
        "title": "Clean Code",
        "author": "Robert C. Martin"
      }
    ]
  }
}
```

#### 14. Process Book Return
```http
PUT /api/v1/orders/{order_id}/return
Authorization: Bearer <token>
Content-Type: application/json

{
  "return_date": "2024-01-24",
  "notes": "Books in good condition"
}
```

**Response (200):**
```json
{
  "success": true,
  "message": "Books returned successfully",
  "data": {
    "order_id": 1,
    "order_status": "Returned",
    "returned_books_count": 3
  }
}
```

#### 15. Update Order Status
```http
PATCH /api/v1/orders/{order_id}/status
Authorization: Bearer <token>
Content-Type: application/json

{
  "status": "Overdue"
}
```

#### 16. Cancel Order
```http
DELETE /api/v1/orders/{order_id}
Authorization: Bearer <token>
```

**Conditions:**
- Chỉ có thể hủy đơn chưa hoàn thành
- Sách phải trở về trạng thái "Available"

---

### 📊 Reports API

#### 17. Get System Statistics
```http
GET /api/v1/reports/statistics
Authorization: Bearer <token>
```

**Response (200):**
```json
{
  "success": true,
  "data": {
    "total_books": 150,
    "available_books": 100,
    "rented_books": 45,
    "damaged_books": 5,
    "total_customers": 120,
    "active_orders": 35,
    "total_orders": 250,
    "revenue_month": 25000000,
    "revenue_year": 280000000,
    "average_rent_duration": 10.5
  }
}
```

#### 18. Get Revenue Report
```http
GET /api/v1/reports/revenue?start_date=2024-01-01&end_date=2024-01-31
Authorization: Bearer <token>
```

**Query Parameters:**
- `start_date`: YYYY-MM-DD
- `end_date`: YYYY-MM-DD

**Response (200):**
```json
{
  "success": true,
  "data": {
    "period": {
      "start_date": "2024-01-01",
      "end_date": "2024-01-31"
    },
    "total_revenue": 25000000,
    "daily_average": 833333,
    "transaction_count": 30,
    "top_books": [
      {
        "book_id": 1,
        "title": "Clean Code",
        "rentals": 15,
        "revenue": 450000
      }
    ]
  }
}
```

#### 19. Get Rental Statistics
```http
GET /api/v1/reports/rentals?category=Programming
Authorization: Bearer <token>
```

**Response (200):**
```json
{
  "success": true,
  "data": {
    "total_rentals": 450,
    "by_category": [
      {
        "category": "Programming",
        "rentals": 120,
        "percentage": 26.7
      }
    ],
    "by_status": {
      "active": 35,
      "completed": 415,
      "overdue": 0
    }
  }
}
```

---

## 🔄 HTTP Status Codes

| Code | Meaning |
|------|---------|
| 200 | OK - Request successful |
| 201 | Created - Resource created |
| 204 | No Content - Successful but no content |
| 400 | Bad Request - Invalid parameters |
| 401 | Unauthorized - Missing/invalid token |
| 403 | Forbidden - Insufficient permissions |
| 404 | Not Found - Resource not found |
| 409 | Conflict - Business logic violation |
| 500 | Server Error - Internal error |

## 📝 Error Response Format

```json
{
  "success": false,
  "message": "Error description",
  "errors": [
    {
      "field": "username",
      "message": "Username is required"
    }
  ]
}
```

## 🧪 Testing dengan cURL

### Login
```bash
curl -X POST http://localhost:5000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin",
    "password": "password123"
  }'
```

### Get Books
```bash
curl -X GET http://localhost:5000/api/v1/books \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### Create Book
```bash
curl -X POST http://localhost:5000/api/v1/books \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "book_code": "B101",
    "title": "The Pragmatic Programmer",
    "author": "David Thomas",
    "category": "Programming",
    "publisher": "Addison-Wesley",
    "publish_year": 2019
  }'
```

## 📚 Rate Limiting

- **Limit:** 1000 requests per hour per IP
- **Header:** `X-RateLimit-Remaining: 999`

## 🔄 Pagination

Endpoints hỗ trợ pagination:

```http
GET /api/v1/books?page=1&limit=20
```

**Response includes:**
```json
{
  "pagination": {
    "current_page": 1,
    "total_pages": 8,
    "total_records": 150,
    "per_page": 20
  }
}
```

## 📖 Versioning

API hiện tại: **v1**

URL format: `http://localhost:5000/api/v1/{endpoint}`

---

**Last Updated:** 2026-05-31 
**API Version:** 1.0.0
