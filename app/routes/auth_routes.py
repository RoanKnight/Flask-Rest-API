from flask import Blueprint, request, jsonify
from datetime import datetime, timedelta
import jwt

from app import db
from app.models import User, UserRole, Customer
from app.schemas.user_schema import UserSchema
from app.config import Config
from werkzeug.security import generate_password_hash

# Create a Blueprint for authentication routes
auth_routes = Blueprint('auth_routes', __name__)
user_schema = UserSchema()

# Function to generate a JWT token for a user
def generate_token(user):
  payload = {
      'user_id': user.id,
      'exp': datetime.utcnow() + timedelta(hours=24)  # Token expiration time
  }
  token = jwt.encode(payload, Config.JWT_USER_TOKEN, algorithm='HS256')
  return token

# Route to handle user registration
@auth_routes.route('/register', methods=['POST'])
def register():
  data = request.get_json()
  if not data:
    return jsonify({"message": "No input data provided"}), 400

  # Remove date_of_birth from data before validation
  date_of_birth_str = data.pop('date_of_birth', None)

  # Validate the input data using the UserSchema
  errors = user_schema.validate(data)
  if errors:
    return jsonify(errors), 400

  # Check if the passwords match
  if data.get('password') != data.get('c_password'):
    return jsonify({"message": "Passwords do not match"}), 400

  # Check if the user already exists
  if User.query.filter_by(email=data.get('email')).first():
    return jsonify({"message": "User already exists"}), 400

  # Create a new User instance
  user = User(
      name=data.get('name'),
      email=data.get('email'),
      phone_number=data.get('phone_number'),
      address=data.get('address'),
      password_hash=generate_password_hash(data.get('password'))
  )

  try:
    # Add the user to the database
    db.session.add(user)
    db.session.commit()
  except Exception as e:
    db.session.rollback()
    return jsonify({"message": "Error creating user"}), 500

  # Create corresponding entry in Customer table
  if not date_of_birth_str:
    return jsonify({"message": "Date of birth is required for customers"}), 400
  try:
    date_of_birth = datetime.strptime(date_of_birth_str, '%Y-%m-%d').date()
  except ValueError:
    return jsonify({"message": "Invalid date format. Use YYYY-MM-DD."}), 400
  customer = Customer(user_id=user.id, date_of_birth=date_of_birth)
  try:
    # Add the customer to the database
    db.session.add(customer)
    db.session.commit()
  except Exception as e:
    db.session.rollback()
    return jsonify({"message": "Error creating customer entry"}), 500

  # Generate a token for the new user
  token = generate_token(user)
  user_data = user_schema.dump(user)

  response = {
      "success": {
          "token": token,
          "user": user_data
      }
  }

  return jsonify(response), 201

# Route to handle user login
@auth_routes.route('/login', methods=['POST'])
def login():
  data = request.get_json()
  if not data:
    return jsonify({"message": "No input data provided"}), 400

  email = data.get('email')
  password = data.get('password')

  if not email or not password:
    return jsonify({"message": "Email and password are required"}), 400

  # Query the user from the database
  user = User.query.filter_by(email=email).first()
  if not user or not user.check_password(password):
    return jsonify({"message": "Invalid email or password"}), 401

  # Generate a token for the logged-in user
  token = generate_token(user)
  user_data = user_schema.dump(user)

  response = {
      "success": {
          "token": token,
          "user": user_data
      }
  }

  return jsonify(response), 200
