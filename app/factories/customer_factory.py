from faker import Faker
from app.models import Customer
from datetime import date

# Initialize the Faker library to generate fake data
faker = Faker()

# Function to create a customer with a specified user_id
def create_customer(user_id):
  # Generate a date of birth as a date object
  dob = faker.date_of_birth(tzinfo=None, minimum_age=18, maximum_age=90)

  # Create a new Customer instance with fake data
  customer = Customer(
      date_of_birth=dob,
      user_id=user_id
  )
  return customer
