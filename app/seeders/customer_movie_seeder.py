from app.models import Customer, Movie, CustomerMovie
from app import db
from app.factories.customer_movie_factory import create_customer_movie
from faker import Faker

faker = Faker()

# Function to seed the customer-movie relationship table
def seed_customer_movies():
  customers = Customer.query.all()
  movies = Movie.query.all()
  customer_movies = []

  # Loop through each customer and assign them two random movies
  for customer in customers:
    # Generate a random sample of two movies
    for movie in faker.random_sample(movies, 2):
      # Create a new CustomerMovie instance and add it to the list
      customer_movies.append(create_customer_movie(customer.id, movie.id))

  db.session.add_all(customer_movies)
  db.session.commit()
