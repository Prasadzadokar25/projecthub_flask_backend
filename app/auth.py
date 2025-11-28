from flask import request, jsonify, current_app
import jwt
from datetime import datetime, timedelta


def generate_jwt(user_id, hours_valid=12):
    """Create a signed JWT for the given user id."""
    payload = {
        'user_id': user_id,
        'exp': datetime.utcnow() + timedelta(hours=hours_valid)
    }
    token = jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm='HS256')
    if isinstance(token, bytes):
        token = token.decode('utf-8')
    return token


def decode_jwt(token):
    """Decode and verify a JWT, returning the payload or raising an exception."""
    return jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])


def register_auth(app):
    """Register a before_request handler on the app to verify JWT for protected routes.

    It uses `Config.PUBLIC_PATHS` from app config to skip protection for public endpoints.
    """

    @app.before_request
    def require_jwt_for_requests():
        # Allow preflight
        if request.method == 'OPTIONS':
            return

        public_paths = app.config.get('PUBLIC_PATHS', ['/','/checkLogin'])
        # Normalize path: strip trailing slash for comparison
        current_path = request.path.rstrip('/')
        if not current_path:  # if path was just '/', keep it as '/'
            current_path = '/'
        
        # Check if current path is in public paths (exact match or normalized)
        if current_path in public_paths or request.path in public_paths:
            return

        auth_header = request.headers.get('Authorization', None)
        if not auth_header:
            return jsonify({'status': 'error', 'message': 'Missing Authorization header'}), 401

        parts = auth_header.split()
        if len(parts) != 2 or parts[0].lower() != 'bearer':
            return jsonify({'status': 'error', 'message': 'Invalid Authorization header format'}), 401

        token = parts[1]
        try:
            payload = decode_jwt(token)
            # expose user id for downstream handlers
            request.user_id = payload.get('user_id')
        except jwt.ExpiredSignatureError:
            return jsonify({'status': 'error', 'message': 'Token has expired'}), 401
        except jwt.InvalidTokenError as e:
            return jsonify({'status': 'error', 'message': f'Invalid token: {str(e)}'}), 401
