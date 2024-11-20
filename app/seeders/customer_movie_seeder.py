from app.models import Customer, Movie, CustomerMovie
from app import db
from app.factories.customer_movie_factory import create_customer_movie
from faker import Faker

faker = Faker()

def seed_customer_movies():
  customers = Customer.query.all()
  movies = Movie.query.all()
  customer_movies = []

  for customer in customers:
    for movie in faker.random_sample(movies, 3):
      customer_movies.append(create_customer_movie(customer.id, movie.id))

  db.session.add_all(customer_movies)
  db.session.commit()
