# 📚 Book Rental System (CLI)

Ứng dụng quản lý cho thuê sách chạy trên giao diện dòng lệnh (CLI), được thiết kế theo kiến trúc **Clean Architecture / DDD** để dễ mở rộng và bảo trì.

---

## ▶️ Chạy chương trình

```bash
pip install sqlalchemy pyodbc python-dotenv
python main.py
```

---

## 📂 Cấu trúc thư mục

```text
book_rental/
|-- .env
|-- main.py
|-- README.md
|-- requirements.txt
|-- application/
|   |-- dto/
|   `-- services/
|       |-- auth_service.py
|       |-- book_service.py
|       |-- customer_service.py
|       |-- order_service.py
|       `-- report_service.py
|-- config/
|   `-- settings.py
|-- database/
|   `-- connection.py
|-- domain/
|   |-- exceptions/
|   |   `-- business_exception.py
|   `-- models/
|       |-- book.py
|       |-- customer.py
|       |-- order.py
|       `-- user.py
|-- infrastructure/
|   |-- db_models/
|   |   |-- base.py
|   |   `-- models.py
|   `-- repositories/
|       |-- book_repository.py
|       |-- customer_repository.py
|       |-- order_repository.py
|       `-- user_repository.py
|-- presentation/
|   `-- cli/
|       |-- admin_menu.py
|       |-- customer_menu.py
|       `-- main_menu.py
|-- shared/
|   |-- constants/
|   `-- utils/
|       `-- logger.py
`-- tests/
```
