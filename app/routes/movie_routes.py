from flask import Blueprint, request, jsonify
from flasgger import swag_from
from app import db
from app.models import Movie, UserRole
from app.schemas.movie_schema import MovieSchema
from app.middleware import token_required, role_required

# Create a Blueprint for movie routes
movie_routes = Blueprint('movie_routes', __name__)
movie_schema = MovieSchema()

# Route to get all movies
@movie_routes.route('/movies', methods=['GET'])
@token_required
@role_required(UserRole.ADMIN, UserRole.CUSTOMER)
@swag_from('../../docs/movies/index.yml')
def index(current_user):
  # Query all movies from the database
  movies = Movie.query.all()
  movie_data = movie_schema.dump(movies, many=True)
  response = {
      "success": {
          "movies": movie_data
      }
  }
  return jsonify(response), 200

# Route to get a specific movie by ID
@movie_routes.route('/movies/<int:id>', methods=['GET'])
@token_required
@role_required(UserRole.ADMIN)
@swag_from('../../docs/movies/show.yml')
def show(current_user, id):
  # Query the movie by ID
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
