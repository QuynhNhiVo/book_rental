from flask import Blueprint
from ..middlewares.auth_middleware import require_role

def create_user_blueprint(user_controller):
    """
    Khởi tạo Blueprint cho các route Khách hàng.
    """
    user_bp = Blueprint('user', __name__)

    @user_bp.route('/books', methods=['GET'])
    @require_role(['Customer'])
    def get_books():
        return user_controller.get_books()

    @user_bp.route('/rentals/create', methods=['POST'])
    @require_role(['Customer'])
    def create_rental():
        return user_controller.create_rental()

    @user_bp.route('/rentals/current', methods=['GET'])
    @require_role(['Customer'])
    def get_current_rentals():
        return user_controller.get_current_rentals()

    @user_bp.route('/rentals/history', methods=['GET'])
    @require_role(['Customer'])
    def get_history():
        return user_controller.get_history()

    @user_bp.route('/dashboard/stats', methods=['GET'])
    @require_role(['Customer'])
    def get_stats():
        """
        Get User Dashboard Statistics
        ---
        tags:
          - User - Dashboard
        security:
          - Bearer: []
        responses:
          200:
            description: User statistics retrieved
        """
        return user_controller.get_dashboard_stats()

    return user_bp
