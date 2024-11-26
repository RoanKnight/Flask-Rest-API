from flask import Blueprint, request, jsonify
from app import db
from app.models import Movie, CustomerMovie, UserRole
from app.schemas.customer_movie_schema import CustomerMovieSchema
from app.schemas.movie_schema import MovieSchema
from app.middleware import token_required, role_required

customer_movie_routes = Blueprint('customer_movie_routes', __name__)
customer_movie_schema = CustomerMovieSchema()

@customer_movie_routes.route('/customerMovies', methods=['GET'])
@token_required
@role_required(UserRole.ADMIN)
def index(current_user):
  customer_movies = CustomerMovie.query.all()
  customer_movies_data = customer_movie_schema.dump(customer_movies, many=True)
  response = {
      "success": {
          "customer_movies": customer_movies_data
      }
  }
  return jsonify(response), 200

@customer_movie_routes.route('/customerMovies/<int:id>', methods=['GET'])
@token_required
@role_required(UserRole.ADMIN)
def show(current_user, id):
  customer_movie = CustomerMovie.query.get(id)
  if not customer_movie:
    return jsonify({"message": "CustomerMovie not found"}), 404

  customer_movie_data = customer_movie_schema.dump(customer_movie)
  response = {
      "success": {
          "customer_movie": customer_movie_data
      }
  }
  return jsonify(response), 200
