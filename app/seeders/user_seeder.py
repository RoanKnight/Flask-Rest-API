from app.factories.user_factory import create_user
from app.models import UserRole, User
from app import db

def seed_users(total_users=50, director_percentage=20):
  num_directors = int(total_users * (director_percentage / 100))
  num_customers = total_users - num_directors

  users = []

  user1 = User(
      name="Test Director",
      email="director@example.com",
      phone_number="1234567890",
      address="123 Director St",
      role=UserRole.DIRECTOR.value
  )
  user1.set_password("password123")
  users.append(user1)

  user2 = User(
      name="Test Customer",
      email="customer@example.com",
      phone_number="0987654321",
      address="456 Customer Ave"
  )
  user2.set_password("password123")
  users.append(user2)

  # Create random users
  for _ in range(num_directors):
    users.append(create_user(UserRole.DIRECTOR))

  for _ in range(num_customers):
    users.append(create_user(UserRole.CUSTOMER))

  db.session.bulk_save_objects(users)
  db.session.commit()
