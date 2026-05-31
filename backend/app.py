from flask import Flask, jsonify
from flask_cors import CORS
from flasgger import Swagger

from src.configs.settings import settings
from src.repositories.user_repository import UserRepository
from src.repositories.book_repository import BookRepository
from src.repositories.customer_repository import CustomerRepository
from src.repositories.order_repository import OrderRepository

from src.services.auth_service import AuthService
from src.services.book_service import BookService
from src.services.customer_service import CustomerService
from src.services.order_service import OrderService
from src.services.report_service import ReportService

from src.controllers.auth_controller import AuthController
from src.controllers.admin_controller import AdminController
from src.controllers.user_controller import UserController

from src.routes.auth_routes import create_auth_blueprint
from src.routes.admin_routes import create_admin_blueprint
from src.routes.user_routes import create_user_blueprint

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = settings.SECRET_KEY
    CORS(app)

    # 1. Khởi tạo Repository (Data Layer)
    user_repo = UserRepository()
    book_repo = BookRepository()
    customer_repo = CustomerRepository()
    order_repo = OrderRepository()

    # 2. Khởi tạo Service (Business Layer)
    auth_service = AuthService(user_repo)
    book_service = BookService(book_repo)
    customer_service = CustomerService(customer_repo)
    order_service = OrderService(order_repo, book_repo, customer_repo)
    report_service = ReportService(book_repo, order_repo, customer_repo)

    # 3. Khởi tạo Controller (Presentation Layer)
    auth_controller = AuthController(auth_service)
    admin_controller = AdminController(book_service, customer_service, order_service, report_service)
    user_controller = UserController(book_service, order_service, report_service)

    # 4. Đăng ký Routes (Blueprints)
    app.register_blueprint(create_auth_blueprint(auth_controller), url_prefix='/api/v1/auth')
    app.register_blueprint(create_admin_blueprint(admin_controller), url_prefix='/api/v1/admin')
    app.register_blueprint(create_user_blueprint(user_controller), url_prefix='/api/v1/user')

    # 5. Cấu hình Swagger
    swagger_template = {
        "swagger": "2.0",
        "info": {
            "title": "Book Rental System API (RBAC)",
            "description": "API cho hệ thống quản lý thuê sách phân quyền.",
            "version": "2.0.0"
        },
        "securityDefinitions": {
            "Bearer": {
                "type": "apiKey",
                "name": "Authorization",
                "in": "header",
                "description": "Nhập theo định dạng: Bearer {token}"
            }
        }
    }
    
    swagger_config = {
        "headers": [],
        "specs": [{"endpoint": 'apispec', "route": '/apispec.json'}],
        "static_url_path": "/flasgger_static",
        "swagger_ui": True,
        "specs_route": "/api-docs"
    }
    Swagger(app, template=swagger_template, config=swagger_config)

    @app.route('/')
    def index():
        return jsonify({'message': 'Book Rental API is running', 'version': '2.0.0'})

    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
