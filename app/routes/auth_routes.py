from flask import Blueprint, request, jsonify
from datetime import datetime, timedelta
import jwt

from app import db
from app.models import User, UserRole
from app.schemas.user_schema import UserSchema
from app.config import Config

auth_routes = Blueprint('auth_routes', __name__)
user_schema = UserSchema()

def generate_token(user):
  payload = {
      'user_id': user.id,
      'exp': datetime.utcnow() + timedelta(hours=24)
  }
  token = jwt.encode(payload, Config.JWT_USER_TOKEN, algorithm='HS256')
  return token


@auth_routes.route('/register', methods=['POST'])
def register():
  data = request.get_json()
  if not data:
    return jsonify({"message": "No input data provided"}), 400

  errors = user_schema.validate(data)
  if errors:
    return jsonify(errors), 400

  if data.get('password') != data.get('c_password'):
    return jsonify({"message": "Passwords do not match"}), 400

  if User.query.filter_by(email=data.get('email')).first():
    return jsonify({"message": "User already exists"}), 400

  role_str = data.get('role', UserRole.CUSTOMER.value)
  try:
    role_enum = UserRole(role_str)
  except ValueError:
    return jsonify({"message": f"Invalid role: {role_str}"}), 400

  user = User(
      name=data.get('name'),
      email=data.get('email'),
      phone_number=data.get('phone_number'),
      address=data.get('address'),
      role=role_enum
  )
  user.set_password(data.get('password'))

  db.session.add(user)
  db.session.commit()

  token = generate_token(user)
  user_data = user_schema.dump(user)

  response = {
      "success": {
          "token": token,
          "user": user_data
      }
  }

  return jsonify(response), 201

@auth_routes.route('/login', methods=['POST'])
def login():
  data = request.get_json()
  if not data:
    return jsonify({"message": "No input data provided"}), 400

  email = data.get('email')
  password = data.get('password')

  if not email or not password:
    return jsonify({"message": "Email and password are required"}), 400

  user = User.query.filter_by(email=email).first()
  if not user or not user.check_password(password):
    return jsonify({"message": "Invalid email or password"}), 401

  token = generate_token(user)
  user_data = user_schema.dump(user)

  response = {
      "success": {
          "token": token,
          "user": user_data
      }
  }

  return jsonify(response), 200
