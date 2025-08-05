import jwt
from flask import current_app, jsonify, request
from datetime import datetime, timezone, timedelta
from functools import wraps

def get_user_from_token():
    token = None
    if "Authorization" in request.headers:
        auth_header = request.headers["Authorization"]
        if auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]
    return jwt.decode(token, current_app.config["SECRET_KEY"], algorithms="HS256")

def generate_token(usuario):
    payload = {'usuario': usuario, 'exp': datetime.now(timezone.utc) + timedelta(hours = 1) }
    token = jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm='HS256')
    return token


def token_mandatory(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if "Authorization" in request.headers:
            auth_header = request.headers["Authorization"]
            if auth_header.startswith("Bearer "):
                token = auth_header.split(" ")[1]
        if not token:
            return jsonify({"error": "Nao tem Token ativo"})
        
        try:
                jwt.decode(token, current_app.config["SECRET_KEY"], algorithms="HS256")
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token Expirado"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Token Invalidox"}), 401
        
        return f(*args, **kwargs)
    return decorated