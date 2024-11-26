from app.factories.user_factory import create_user
from app.models import UserRole, User
from app import db

# Seed users function to create a specific Test Director, Test Customer, and random Directors and Customers
def seed_users(total_users=50, director_percentage=20):
  # Calculate the number of Directors and Customers
  num_directors = int(total_users * (director_percentage / 100))
  num_customers = total_users - num_directors

  users = []

  # Create a specific Test Director
  user1 = User(
      name="Test Director",
      email="director@example.com",
      phone_number="1234567890",
      address="123 Director St",
      role=UserRole.DIRECTOR.value
  )
  user1.set_password("password123")
  users.append(user1)

  # Create a specific Test Customer
  user2 = User(
      name="Test Customer",
      email="customer@example.com",
      phone_number="0987654321",
      address="456 Customer Ave",
      role=UserRole.CUSTOMER.value
  )
  user2.set_password("password123")
  users.append(user2)
  
  user3 = User(
      name="Test Admin",
      email="admin@example.com",
      phone_number="0987654321",
      address="456 Admin Ave",
      role=UserRole.ADMIN.value
  )
  user3.set_password("password123")
  users.append(user3)

  # Create random Directors
  for _ in range(num_directors):
    users.append(create_user(UserRole.DIRECTOR))

  # Create random Customers
  for _ in range(num_customers):
    users.append(create_user(UserRole.CUSTOMER))

  db.session.add_all(users)
  db.session.commit()
