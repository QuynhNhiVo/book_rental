from flask import Blueprint

def create_auth_blueprint(auth_controller):
    """
    Khởi tạo Blueprint cho các route xác thực.
    """
    auth_bp = Blueprint('auth', __name__)

    @auth_bp.route('/login', methods=['POST'])
    def login():
        """
        User Login
        ---
        tags:
          - Authentication
        parameters:
          - name: body
            in: body
            required: true
            schema:
              type: object
              properties:
                username:
                  type: string
                  example: admin
                password:
                  type: string
                  example: password123
        responses:
          200:
            description: Login successful
          401:
            description: Invalid credentials
        """
        return auth_controller.login()

    return auth_bp
