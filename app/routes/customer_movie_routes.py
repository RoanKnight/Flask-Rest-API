from flask import Blueprint, request, jsonify
from flasgger import swag_from
from app import db
from app.models import Movie, CustomerMovie, UserRole
from app.schemas.customer_movie_schema import CustomerMovieSchema
from app.schemas.movie_schema import MovieSchema
from app.middleware import token_required, role_required

# Create a Blueprint for customer-movie routes
customer_movie_routes = Blueprint('customer_movie_routes', __name__)
customer_movie_schema = CustomerMovieSchema()

# Route to get all customer-movies
@customer_movie_routes.route('/customerMovies', methods=['GET'])
@token_required
@role_required(UserRole.ADMIN)
@swag_from('../../docs/customerMovies/index.yml')
def index(current_user):
  # Query all customer-movie from the database
  customer_movies = CustomerMovie.query.all()
  customer_movies_data = customer_movie_schema.dump(customer_movies, many=True)
  response = {
      "success": {
          "customer_movies": customer_movies_data
      }
  }
  return jsonify(response), 200

# Route to get a specific customer-movie by ID
@customer_movie_routes.route('/customerMovies/<int:id>', methods=['GET'])
@token_required
@role_required(UserRole.ADMIN)
@swag_from('../../docs/customerMovies/show.yml')
def show(current_user, id):
  # Query the customer-movie by ID
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
