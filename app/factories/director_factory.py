from faker import Faker
from app.models import Director

faker = Faker()

def create_director(user_id):
  director = Director(
      website_url=faker.url(),
      user_id=user_id
  )
  return director
