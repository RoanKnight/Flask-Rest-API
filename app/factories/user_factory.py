from faker import Faker
from app.models import User, UserRole
from app import db

faker = Faker()

def create_user(role):
  user = User(
      name=faker.name(),
      email=faker.unique.email(),
      phone_number=faker.phone_number(),
      address=faker.address(),
      role=role.value
  )
  user.set_password(faker.password())
  return user
