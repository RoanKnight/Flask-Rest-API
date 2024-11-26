from app.models import UserRole, User, Customer
from app import db
from app.factories.customer_factory import create_customer

# Function to seed customers
def seed_customers():
  # Get all users with the role of customer
  users = User.query.filter_by(role=UserRole.CUSTOMER).all()

  # Create a customer for each user
  customers = [create_customer(user.id) for user in users]

  db.session.add_all(customers)
  db.session.commit()
