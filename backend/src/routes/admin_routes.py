from flask import Blueprint
from ..middlewares.auth_middleware import require_role

def create_admin_blueprint(admin_controller):
    """
    Khởi tạo Blueprint cho các route Admin.
    """
    admin_bp = Blueprint('admin', __name__)

    @admin_bp.route('/books', methods=['GET'])
    @require_role(['Admin'])
    def get_books():
        """
        List All Books (Admin)
        ---
        tags:
          - Admin - Books
        security:
          - Bearer: []
        responses:
          200:
            description: List of all books
        """
        return admin_controller.get_all_books()

    @admin_bp.route('/books', methods=['POST'])
    @require_role(['Admin'])
    def create_book():
        """
        Add New Book
        ---
        tags:
          - Admin - Books
        security:
          - Bearer: []
        parameters:
          - name: body
            in: body
            required: true
            schema:
              type: object
              properties:
                book_code:
                  type: string
                title:
                  type: string
                author:
                  type: string
        responses:
          201:
            description: Book created
        """
        return admin_controller.create_book()

    @admin_bp.route('/reports/statistics', methods=['GET'])
    @require_role(['Admin'])
    def get_stats():
        """
        Get System Statistics
        ---
        tags:
          - Admin - Reports
        security:
          - Bearer: []
        responses:
          200:
            description: System statistics retrieved
        """
        return admin_controller.get_stats()

    @admin_bp.route('/orders', methods=['GET'])
    @require_role(['Admin'])
    def get_orders():
        return admin_controller.get_all_orders()

    @admin_bp.route('/orders/<int:id>/return', methods=['PUT'])
    @require_role(['Admin'])
    def return_book(id):
        return admin_controller.return_book(id)
        
    @admin_bp.route('/customers', methods=['GET'])
    @require_role(['Admin'])
    def get_customers():
        return admin_controller.get_all_customers()

    return admin_bp
