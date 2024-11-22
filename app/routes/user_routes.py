from flask import Blueprint, request, jsonify
from app import db
from app.models import User, UserRole, Director, Customer, Movie, CustomerMovie
from app.schemas.user_schema import UserSchema
from app.config import Config
from app.middleware import token_required, role_required

user_routes = Blueprint('user_routes', __name__)
user_schema = UserSchema()

@user_routes.route('/users', methods=['GET'])
@token_required
@role_required(UserRole.DIRECTOR)
def index(current_user):
  users = User.query.all()
  users_data = user_schema.dump(users, many=True)
  response = {
      "success": {
          "users": users_data
      }
  }
  return jsonify(response), 200

@user_routes.route('/users/<int:id>', methods=['GET'])
@token_required
@role_required(UserRole.DIRECTOR)
def show(current_user, id):
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

@user_routes.route('/users/showProfile', methods=['GET'])
@token_required
def show_profile(current_user):
  user = User.query.get(current_user.id)
  if not user:
    return jsonify({"message": "User not found"}), 404

  user_data = user_schema.dump(user)
  response = {
      "success": {
          "user": user_data
      }
  }
  return jsonify(response), 200

@user_routes.route('/users/update', methods=['PUT'])
@token_required
def update_user(current_user):
  user = User.query.get(current_user.id)
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

@user_routes.route('/users/delete/<int:id>', methods=['DELETE'])
@token_required
@role_required(UserRole.DIRECTOR)
def delete_user(current_user, id):
  user = User.query.get(id)
  if not user:
    return jsonify({"message": "User not found"}), 404

  # Mark the user as deleted
  user.deleted = True

  if user.role == UserRole.CUSTOMER:
    customer = Customer.query.filter_by(user_id=user.id).first()
    if customer:
      customer.deleted = True
      # Mark all related CustomerMovie entries as deleted
      customer_movies = CustomerMovie.query.filter_by(
          customer_id=customer.id).all()
      for customer_movie in customer_movies:
        customer_movie.deleted = True
  elif user.role == UserRole.DIRECTOR:
    director = Director.query.filter_by(user_id=user.id).first()
    if director:
      director.deleted = True
      # Mark all related movies as deleted
      movies = Movie.query.filter_by(director_id=director.id).all()
      for movie in movies:
        movie.deleted = True
        # Mark all related CustomerMovie entries as deleted
        customer_movies = CustomerMovie.query.filter_by(
            movie_id=movie.id).all()
        for customer_movie in customer_movies:
          customer_movie.deleted = True

  db.session.commit()
  return jsonify({"message": "User and related records deleted"}), 200

@user_routes.route('/users/restore/<int:id>', methods=['PUT'])
@token_required
@role_required(UserRole.DIRECTOR)
def restore_user(current_user, id):
  user = User.query.get(id)
  if not user:
    return jsonify({"message": "User not found"}), 404

  # Mark the user as not deleted
  user.deleted = False

  if user.role == UserRole.CUSTOMER:
    customer = Customer.query.filter_by(user_id=user.id).first()
    if customer:
      customer.deleted = False
      # Mark all related CustomerMovie entries as not deleted
      customer_movies = CustomerMovie.query.filter_by(
          customer_id=customer.id).all()
      for customer_movie in customer_movies:
        customer_movie.deleted = False
  elif user.role == UserRole.DIRECTOR:
    director = Director.query.filter_by(user_id=user.id).first()
    if director:
      director.deleted = False
      # Mark all related movies as not deleted
      movies = Movie.query.filter_by(director_id=director.id).all()
      for movie in movies:
        movie.deleted = False
        # Mark all related CustomerMovie entries as not deleted
        customer_movies = CustomerMovie.query.filter_by(
            movie_id=movie.id).all()
        for customer_movie in customer_movies:
          customer_movie.deleted = False

  db.session.commit()
  return jsonify({"message": "User and related records restored"}), 200
