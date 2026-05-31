import jwt
from datetime import datetime, timedelta
from functools import wraps
from flask import request, jsonify, g
from ..configs.settings import settings

def create_auth_token(user) -> str:
    """Tạo JWT Token cho người dùng."""
    payload = {
        'user_id': user.user_id,
        'username': user.username,
        'role': user.role,
        'customer_id': user.customer_id,
        'exp': datetime.utcnow() + timedelta(hours=24),
        'iat': datetime.utcnow()
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')

def get_request_context():
    """Phân tích Token từ Header Authorization."""
    auth_header = request.headers.get('Authorization', '')
    if not auth_header or not auth_header.startswith('Bearer '):
        return None
    
    token = auth_header.split()[1]
    try:
        return jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
    except Exception:
        return None

def require_role(allowed_roles):
    """Decorator để kiểm tra quyền truy cập của người dùng."""
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            ctx = get_request_context()
            if ctx is None or ctx.get('role') not in allowed_roles:
                return jsonify({'success': False, 'message': 'Bạn không có quyền thực hiện hành động này.'}), 401
            
            # Lưu thông tin user vào biến g (global) của Flask để sử dụng trong controller
            g.auth_context = ctx
            return fn(*args, **kwargs)
        return wrapper
    return decorator
