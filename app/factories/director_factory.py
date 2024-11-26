from faker import Faker
from app.models import Director

# Initialize the Faker library to generate fake data
faker = Faker()

# Function to create a director with a specified user_id
def create_director(user_id):
  # Create a new Director instance with fake data
  director = Director(
      website_url=faker.url(),
      user_id=user_id
  )
  return director
