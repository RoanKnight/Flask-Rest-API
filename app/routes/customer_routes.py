from flask import Blueprint, request, jsonify, current_app
from flasgger import swag_from
from app import db
from app.email import send_email
from app.models import UserRole, Customer, CustomerMovie, Movie
from app.schemas.customer_schema import CustomerSchema
from app.schemas.movie_schema import MovieSchema
from app.middleware import token_required, role_required
from datetime import datetime, timedelta

# Create a Blueprint for customer routes
customer_routes = Blueprint('customer_routes', __name__)
customer_schema = CustomerSchema()
movie_schema = MovieSchema()

# Route to get all customers
@customer_routes.route('/customers', methods=['GET'])
@token_required
@role_required(UserRole.ADMIN)
@swag_from('../../docs/customers/index.yml')
def index(current_user):
  # Query all customers from the database
  customers = Customer.query.all()
  customers_data = customer_schema.dump(customers, many=True)
  response = {
      "success": {
          "customers": customers_data
      }
  }
  return jsonify(response), 200

# Route to get a specific customer by ID
@customer_routes.route('/customers/<int:id>', methods=['GET'])
@token_required
@role_required(UserRole.ADMIN)
@swag_from('../../docs/customers/show.yml')
def show(current_user, id):
  # Query the customer by ID
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

@customer_routes.route('/customers/<int:id>/showMovies', methods=['GET'])
@token_required
@role_required(UserRole.CUSTOMER, UserRole.ADMIN)
@swag_from('../../docs/customers/showMovies.yml')
def show_movies(current_user, id):
  # Check if the current user is a customer and if the ID in the URL matches the current user's ID
  if current_user.role == UserRole.CUSTOMER:
    customer = Customer.query.filter_by(user_id=current_user.id).first()
    if not customer or customer.id != id:
      return jsonify({"message": "Unauthorized access"}), 403
  else:
    # For admins, use the provided customer ID
    customer = Customer.query.get(id)
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
      movie_data['due'] = cm.due.strftime('%a, %d %b %Y')
      movie_data['extended'] = cm.extended
      movies_data.append(movie_data)

  response = {
      "success": {
          "movies": movies_data
      }
  }
  return jsonify(response), 200

# Route to update the current customer's information
@customer_routes.route('/customers/<int:id>/updateCustomer', methods=['PUT'])
@token_required
@role_required(UserRole.CUSTOMER)
@swag_from('../../docs/customers/update.yml')
def update_customer(current_user, id):
  # Check if the ID in the URL matches the current customer's ID
  customer = Customer.query.filter_by(user_id=current_user.id).first()
  if not customer or customer.id != id:
    return jsonify({"message": "Unauthorized access"}), 403

  # Get the input data from the request
  data = request.get_json()
  if not data:
    return jsonify({"message": "No input data provided"}), 400

  # Update the date of birth if provided
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

# Route to rent a movie for the current customer
@customer_routes.route('/customers/<int:id>/rentMovie', methods=['POST'])
@token_required
@role_required(UserRole.CUSTOMER)
def rent_movie(current_user, id):
  # Check if the ID in the URL matches the current customer's ID
  customer = Customer.query.filter_by(user_id=current_user.id).first()
  if not customer or customer.id != id:
    return jsonify({"message": "Unauthorized access"}), 403

  # Get the input data from the request
  data = request.get_json()
  if not data:
    return jsonify({"message": "No input data provided"}), 400

  movie_id = data.get('movie_id')
  movie = Movie.query.get(movie_id)
  if not movie:
    return jsonify({"message": "Movie not found"}), 404

  # Check if the movie is already rented
  customer_movie = CustomerMovie.query.filter_by(
      customer_id=customer.id, movie_id=movie.id).first()
  if customer_movie:
    return jsonify({"message": "Movie already rented"}), 400

  # Create a new CustomerMovie entry with a due date 30 days from now
  due_date = datetime.now() + timedelta(days=30)
  customer_movie = CustomerMovie(
      customer_id=customer.id,
      movie_id=movie.id,
      due=due_date,
      extended=False
  )
  db.session.add(customer_movie)
  db.session.commit()

  # Get the email of the user corresponding to the current customer
  user_email = customer.user.email

  send_email(
      "Movie rented successfully",
      current_app.config['MAIL_DEFAULT_SENDER'],
      recipients=[user_email],
      text_body="You have rented a movie successfully.",
      html_body="<p>You have rented a movie successfully.</p>",
      attachments=None,
      sync=False
  )

  response = {
      "success": {
          "message": "Movie rented successfully"
      }
  }
  return jsonify(response), 201
