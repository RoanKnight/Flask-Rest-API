from faker import Faker
from app.models import CustomerMovie
from datetime import datetime, timedelta

# Initialize the Faker library to generate fake data
faker = Faker()

# Function to create a customer-movie relationship with specified customer_id and movie_id
def create_customer_movie(customer_id, movie_id):
  # Generate a due date within the next 30 days
  due_date = faker.date_time_between(start_date="now", end_date="+30d")

  # Create a new CustomerMovie instance with fake data
  customer_movie = CustomerMovie(
      customer_id=customer_id,
      movie_id=movie_id,
      due=due_date,
      extended=faker.boolean()
  )
  return customer_movie
