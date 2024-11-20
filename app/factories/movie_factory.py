from faker import Faker
from app.models import Movie
from datetime import datetime

faker = Faker()

def create_movie(director_id):
  movie = Movie(
      title=faker.catch_phrase(),
      duration=faker.random_int(min=60, max=180),
      rating=faker.random_int(min=1, max=10),
      year=faker.year(),
      director_id=director_id
  )
  return movie
