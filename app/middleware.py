from functools import wraps
from flask import request, jsonify
import jwt
from app.models import User, UserRole
from app.config import Config

# Decorator to check if a valid token is provided in the request headers
def token_required(f):
  @wraps(f)
  def decorated(*args, **kwargs):
    # Get the Authorization header from the request
    auth_header = request.headers.get('Authorization', None)
    if not auth_header:
      return jsonify({"message": "Token is missing!"}), 401

    # Split the header into parts
    parts = auth_header.split()
    if len(parts) != 2 or parts[0].lower() != 'bearer':
      return jsonify({"message": "Invalid authorization header format!"}), 401

    token = parts[1]
    try:
      # Decode the token to get the user data
      data = jwt.decode(token, Config.JWT_USER_TOKEN, algorithms=['HS256'])
      # Query the user from the database
      current_user = User.query.get(data['user_id'])
      if not current_user:
        return jsonify({"message": "User not found!"}), 401
    except jwt.ExpiredSignatureError:
      return jsonify({"message": "Token has expired!"}), 401
    except jwt.InvalidTokenError:
      return jsonify({"message": "Token is invalid!"}), 401

    # Pass the current user to the decorated function
    return f(current_user, *args, **kwargs)
  return decorated

# Decorator to check if the current user has the required role
def role_required(role):
  def decorator(f):
    @wraps(f)
    def decorated_function(current_user, *args, **kwargs):
      # Check if the user's role matches the required role
      if current_user.role != role:
        return jsonify({"message": "You do not have permission to access this resource."}), 403
      return f(current_user, *args, **kwargs)
    return decorated_function
  return decorator
