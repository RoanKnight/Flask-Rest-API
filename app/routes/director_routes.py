from flask import Blueprint, request, jsonify
from app import db
from app.models import UserRole, Director, Movie
from app.schemas.director_schema import DirectorSchema
from app.schemas.movie_schema import MovieSchema
from app.middleware import token_required, role_required
from datetime import datetime
import random

# Create a Blueprint for director routes
director_routes = Blueprint('director_routes', __name__)
director_schema = DirectorSchema()
movie_schema = MovieSchema()

# Route to get all directors
@director_routes.route('/directors', methods=['GET'])
@token_required
@role_required(UserRole.ADMIN)
def index(current_user):
  # Query all directors from the database
  directors = Director.query.all()
  directors_data = director_schema.dump(directors, many=True)
  response = {
      "success": {
          "directors": directors_data
      }
  }
  return jsonify(response), 200

# Route to get a specific director by ID
@director_routes.route('/directors/<int:id>', methods=['GET'])
@token_required
@role_required(UserRole.ADMIN)
def show(current_user, id):
  # Query the director by ID
  director = Director.query.get(id)
  if not director:
    return jsonify({"message": "Director not found"}), 404

  director_data = director_schema.dump(director)
  response = {
      "success": {
          "director": director_data
      }
  }
  return jsonify(response), 200

# Route to show the movies created by the current director
@director_routes.route('/directors/<int:id>/showMovies', methods=['GET'])
@token_required
def show_movies(current_user, id):
    # Check if the ID in the URL matches the current director's ID
  director = Director.query.filter_by(user_id=current_user.id).first()
  if not director or director.id != id:
    return jsonify({"message": "Unauthorized access"}), 403

  # Get all movies for the director
  movies = Movie.query.filter_by(director_id=director.id).all()

  movies_data = movie_schema.dump(movies, many=True)
  response = {
      "success": {
          "movies": movies_data
      }
  }
  return jsonify(response), 200

# Route to update the current director's information
@director_routes.route('/directors/<int:id>/updateDirector', methods=['PUT'])
@token_required
@role_required(UserRole.DIRECTOR)
def update_director(current_user, id):
  # Check if the ID in the URL matches the current director's ID
  director = Director.query.filter_by(user_id=current_user.id).first()
  if not director or director.id != id:
    return jsonify({"message": "Unauthorized access"}), 403

  data = request.get_json()
  if not data:
    return jsonify({"message": "No input data provided"}), 400

  # Update the website URL if provided
  website_url = data.get('website_url')
  if website_url:
    director.website_url = website_url

  db.session.commit()
  director_data = director_schema.dump(director)
  response = {
      "success": {
          "director": director_data
      }
  }
  return jsonify(response), 200

# Route to create a new movie for the current director
@director_routes.route('/directors/<int:id>/createMovie', methods=['POST'])
@token_required
@role_required(UserRole.DIRECTOR)
def create_movie(current_user, id):
  # Check if the ID in the URL matches the current director's ID
  director = Director.query.filter_by(user_id=current_user.id).first()
  if not director or director.id != id:
    return jsonify({"message": "Unauthorized access"}), 403

  data = request.get_json()
  if not data:
    return jsonify({"message": "No input data provided"}), 400

  # Generate a random rating between 1 and 10
  rating = random.randint(1, 10)

  # Set the year to the current year
  current_year = datetime.now().year

  # Create a new Movie instance
  movie = Movie(
      title=data['title'],
      duration=data['duration'],
      rating=rating,
      year=current_year,
      director_id=director.id
  )
  db.session.add(movie)
  db.session.commit()

  movie_data = movie_schema.dump(movie)
  response = {
      "success": {
          "movie": movie_data
      }
  }
  return jsonify(response), 201
