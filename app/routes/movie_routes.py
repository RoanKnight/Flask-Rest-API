from flask import Blueprint, request, jsonify
from app import db
from app.models import Movie, UserRole
from app.schemas.movie_schema import MovieSchema
from app.middleware import token_required, role_required
from datetime import datetime
import random

movie_routes = Blueprint('movie_routes', __name__)
movie_schema = MovieSchema()

@movie_routes.route('/movies', methods=['GET'])
@token_required
@role_required(UserRole.DIRECTOR)
def index(current_user):
  movies = Movie.query.all()
  movie_data = movie_schema.dump(movies, many=True)
  response = {
      "success": {
          "movies": movie_data
      }
  }
  return jsonify(response), 200

@movie_routes.route('/movies/<int:id>', methods=['GET'])
@token_required
@role_required(UserRole.DIRECTOR)
def show(current_user, id):
  movie = Movie.query.get(id)
  if not movie:
    return jsonify({"message": "Movie not found"}), 404

  movie_data = movie_schema.dump(movie)
  response = {
      "success": {
          "movie": movie_data
      }
  }
  return jsonify(response), 200

@movie_routes.route('/movies', methods=['POST'])
@token_required
@role_required(UserRole.DIRECTOR)
def store(current_user):
  data = request.get_json()

  # Generate a random rating between 1 and 10
  rating = random.randint(1, 10)

  # Set the year to the current year
  current_year = datetime.now().year

  movie = Movie(
      title=data['title'],
      duration=data['duration'],
      rating=rating,
      year=current_year,
      director_id=current_user.id
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
