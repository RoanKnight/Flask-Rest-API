from flask import Blueprint, request, jsonify
from flasgger import swag_from
from app import db
from app.models import User, UserRole, Director, Customer, Movie, CustomerMovie
from app.schemas.user_schema import UserSchema
from app.config import Config
from app.middleware import token_required, role_required

# Create a Blueprint for user routes
user_routes = Blueprint('user_routes', __name__)
user_schema = UserSchema()

# Route to get all users
@user_routes.route('/users', methods=['GET'])
@token_required
@role_required(UserRole.ADMIN)
@swag_from('../../docs/users.yml')
def index(current_user):
  # Query all users from the database
  users = User.query.all()
  users_data = user_schema.dump(users, many=True)
  response = {
      "success": {
          "users": users_data
      }
  }
  return jsonify(response), 200

# Route to get a specific user by ID
@user_routes.route('/users/<int:id>', methods=['GET'])
@token_required
@role_required(UserRole.ADMIN)
def show(current_user, id):
  # Query the user by ID
  user = User.query.get(id)
  if not user:
    return jsonify({"message": "User not found"}), 404

  user_data = user_schema.dump(user)
  response = {
      "success": {
          "user": user_data
      }
  }
  return jsonify(response), 200

# Route to show the profile of the current user
@user_routes.route('/users/<int:id>/showProfile', methods=['GET'])
@token_required
def show_profile_by_id(current_user, id):
    # Check if the ID in the URL matches the current user's ID
  if current_user.id != id:
    return jsonify({"message": "Unauthorized access"}), 403

  # Query the current user by ID
  user = User.query.get(id)
  if not user:
    return jsonify({"message": "User not found"}), 404

  user_data = user_schema.dump(user)
  response = {
      "success": {
          "user": user_data
      }
  }
  return jsonify(response), 200

# Route to update a the current user's profile
@user_routes.route('/users/<int:id>/update', methods=['PUT'])
@token_required
def update_user(current_user, id):
    # Check if the ID in the URL matches the current user's ID
  if current_user.id != id:
    return jsonify({"message": "Unauthorized access"}), 403

  # Query the current user by ID
  user = User.query.get(id)
  if not user:
    return jsonify({"message": "User not found"}), 404

  data = request.get_json()
  if not data:
    return jsonify({"message": "No input data provided"}), 400

  # Update only allowed fields
  user.name = data.get('name', user.name)
  user.email = data.get('email', user.email)
  user.phone_number = data.get('phone_number', user.phone_number)
  user.address = data.get('address', user.address)

  db.session.commit()
  user_data = user_schema.dump(user)
  response = {
      "success": {
          "user": user_data
      }
  }
  return jsonify(response), 200

# Helper function to mark a user and related records as deleted or not deleted
def mark_user_and_related_records(user, deleted):
  user.deleted = deleted

  if user.role == UserRole.CUSTOMER:
    customer = Customer.query.filter_by(user_id=user.id).first()
    if customer:
      customer.deleted = deleted
      # Mark all related CustomerMovie entries
      customer_movies = CustomerMovie.query.filter_by(
          customer_id=customer.id).all()
      for customer_movie in customer_movies:
        customer_movie.deleted = deleted
  elif user.role == UserRole.DIRECTOR:
    director = Director.query.filter_by(user_id=user.id).first()
    if director:
      director.deleted = deleted
      # Mark all related movies
      movies = Movie.query.filter_by(director_id=director.id).all()
      for movie in movies:
        movie.deleted = deleted
        # Mark all related CustomerMovie entries
        customer_movies = CustomerMovie.query.filter_by(
            movie_id=movie.id).all()
        for customer_movie in customer_movies:
          customer_movie.deleted = deleted

# Route to delete a user and related records
@user_routes.route('/users/<int:id>/delete', methods=['DELETE'])
@token_required
@role_required(UserRole.ADMIN)
def delete_user(current_user, id):
  # Query the user by ID
  user = User.query.get(id)
  if not user:
    return jsonify({"message": "User not found"}), 404

  # Prevent admins from deleting themselves
  if user.id == current_user.id and user.role == UserRole.ADMIN:
    return jsonify({"message": "Admins cannot delete themselves"}), 403

  # Mark the user and related records as deleted
  mark_user_and_related_records(user, True)

  db.session.commit()
  return jsonify({"message": "User and related records deleted"}), 200

# Route to restore a user and related records
@user_routes.route('/users/<int:id>/restore', methods=['PUT'])
@token_required
@role_required(UserRole.ADMIN)
def restore_user(current_user, id):
  # Query the user by ID
  user = User.query.get(id)
  if not user:
    return jsonify({"message": "User not found"}), 404

  # Mark the user and related records as not deleted
  mark_user_and_related_records(user, False)

  db.session.commit()
  return jsonify({"message": "User and related records restored"}), 200
