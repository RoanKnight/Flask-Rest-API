from flask import Blueprint, request, jsonify
from app import db
from app.models import UserRole, Customer, CustomerMovie, Movie
from app.schemas.customer_schema import CustomerSchema
from app.schemas.movie_schema import MovieSchema
from app.middleware import token_required, role_required
from datetime import datetime, timedelta

customer_routes = Blueprint('customer_routes', __name__)
customer_schema = CustomerSchema()
movie_schema = MovieSchema()

@customer_routes.route('/customers', methods=['GET'])
@token_required
@role_required(UserRole.ADMIN)
def index(current_user):
  customers = Customer.query.all()
  customers_data = customer_schema.dump(customers, many=True)
  response = {
      "success": {
          "customers": customers_data
      }
  }
  return jsonify(response), 200

@customer_routes.route('/customers/<int:id>', methods=['GET'])
@token_required
@role_required(UserRole.ADMIN)
def show(current_user, id):
  customer = Customer.query.get(id)
  if not customer:
    return jsonify({"message": "Customer not found"}), 404

  customer_data = customer_schema.dump(customer)
  response = {
      "success": {
          "customer": customer_data
      }
  }
  return jsonify(response), 200

@customer_routes.route('/customers/showMovies', methods=['GET'])
@token_required
@role_required(UserRole.CUSTOMER)
def show_movies(current_user):
  customer = Customer.query.filter_by(user_id=current_user.id).first()
  if not customer:
    return jsonify({"message": "Customer not found"}), 404

  # Get all CustomerMovie entries for the customer
  customer_movies = CustomerMovie.query.filter_by(
      customer_id=customer.id).all()

  # Extract movie details along with the extra fields from the pivot table
  movies_data = []
  for cm in customer_movies:
    movie = Movie.query.get(cm.movie_id)
    if movie:
      movie_data = movie_schema.dump(movie)
      movie_data['due'] = cm.due.strftime(
          '%a, %d %b %Y')
      movie_data['extended'] = cm.extended
      movies_data.append(movie_data)

  response = {
      "success": {
          "movies": movies_data
      }
  }
  return jsonify(response), 200

@customer_routes.route('/customers/updateCustomer', methods=['PUT'])
@token_required
@role_required(UserRole.CUSTOMER)
def update_customer(current_user):
  data = request.get_json()
  if not data:
    return jsonify({"message": "No input data provided"}), 400

  customer = Customer.query.filter_by(user_id=current_user.id).first()
  if not customer:
    return jsonify({"message": "Customer not found"}), 404

  date_of_birth_str = data.get('date_of_birth')
  if date_of_birth_str:
    try:
      date_of_birth = datetime.strptime(date_of_birth_str, '%Y-%m-%d').date()
      customer.date_of_birth = date_of_birth
    except ValueError:
      return jsonify({"message": "Invalid date format. Use YYYY-MM-DD."}), 400

  db.session.commit()
  customer_data = customer_schema.dump(customer)
  response = {
      "success": {
          "customer": customer_data
      }
  }
  return jsonify(response), 200

@customer_routes.route('/customers/rentMovie', methods=['POST'])
@token_required
@role_required(UserRole.CUSTOMER)
def rent_movie(current_user):
  data = request.get_json()
  if not data:
    return jsonify({"message": "No input data provided"}), 400

  customer = Customer.query.filter_by(user_id=current_user.id).first()
  if not customer:
    return jsonify({"message": "Customer not found"}), 404

  movie_id = data.get('movie_id')
  movie = Movie.query.get(movie_id)
  if not movie:
    return jsonify({"message": "Movie not found"}), 404

  # Check if the movie is already rented
  customer_movie = CustomerMovie.query.filter_by(
      customer_id=customer.id, movie_id=movie.id).first()
  if customer_movie:
    return jsonify({"message": "Movie already rented"}), 400

  # Create a new CustomerMovie entry with a due date 7 days from now
  due_date = datetime.now() + timedelta(days=30)
  customer_movie = CustomerMovie(
      customer_id=customer.id,
      movie_id=movie.id,
      due=due_date,
      extended=False
  )
  db.session.add(customer_movie)
  db.session.commit()

  response = {
      "success": {
          "message": "Movie rented successfully"
      }
  }
  return jsonify(response), 201
