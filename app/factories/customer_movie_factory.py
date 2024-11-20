from faker import Faker
from app.models import CustomerMovie
from datetime import datetime, timedelta

faker = Faker()

def create_customer_movie(customer_id, movie_id):
  due_date = faker.date_time_between(start_date="now", end_date="+30d")

  customer_movie = CustomerMovie(
      customer_id=customer_id,
      movie_id=movie_id,
      due=due_date,
      extended=faker.boolean()
  )
  return customer_movie
