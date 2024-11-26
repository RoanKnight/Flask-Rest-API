from faker import Faker
from app.models import User, UserRole
from app import db

# Initialize the Faker library to generate fake data
faker = Faker()

# Function to create a user with a specified role
def create_user(role):
  # Create a new User instance with fake data
  user = User(
      name=faker.name(),
      email=faker.unique.email(),
      phone_number=faker.phone_number(),
      address=faker.address(),
      role=role.value
  )
  # Set a fake password for the user
  user.set_password(faker.password())
  return user