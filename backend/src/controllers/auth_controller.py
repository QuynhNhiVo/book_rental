from flask import request, jsonify
from ..middlewares.auth_middleware import create_auth_token

class AuthController:
    """
    Controller xử lý các yêu cầu liên quan đến xác thực.
    """
    def __init__(self, auth_service):
        self.auth_service = auth_service

    def login(self):
        try:
            data = request.get_json(silent=True) or {}
            user = self.auth_service.login(data.get('username'), data.get('password'))
            
            token = create_auth_token(user)
            return jsonify({
                'success': True,
                'data': {
                    'token': token,
                    'user_id': user.user_id,
                    'username': user.username,
                    'role': user.role,
                    'customer_id': user.customer_id
                }
            })
        except Exception as e:
            return jsonify({'success': False, 'message': str(e)}), 401
