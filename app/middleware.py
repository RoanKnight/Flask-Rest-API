from functools import wraps
from flask import request, jsonify
import jwt
from app.models import User, UserRole
from app.config import Config

def token_required(f):
  @wraps(f)
  def decorated(*args, **kwargs):
    auth_header = request.headers.get('Authorization', None)
    if not auth_header:
      return jsonify({"message": "Token is missing!"}), 401

    parts = auth_header.split()
    if len(parts) != 2 or parts[0].lower() != 'bearer':
      return jsonify({"message": "Invalid authorization header format!"}), 401

    token = parts[1]
    try:
      data = jwt.decode(token, Config.JWT_USER_TOKEN, algorithms=['HS256'])
      current_user = User.query.get(data['user_id'])
      if not current_user:
        return jsonify({"message": "User not found!"}), 401
    except jwt.ExpiredSignatureError:
      return jsonify({"message": "Token has expired!"}), 401
    except jwt.InvalidTokenError:
      return jsonify({"message": "Token is invalid!"}), 401

    return f(current_user, *args, **kwargs)
  return decorated

def role_required(role):
  def decorator(f):
    @wraps(f)
    def decorated_function(current_user, *args, **kwargs):
      if current_user.role != role:
        return jsonify({"message": "You do not have permission to access this resource."}), 403
      return f(current_user, *args, **kwargs)
    return decorated_function
  return decorator
