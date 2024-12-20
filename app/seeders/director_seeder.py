from app.models import UserRole, User, Director
from app import db
from app.factories.director_factory import create_director

# Seed directors function to create a Director for each user with the role of director
def seed_directors():
  # Get all users with the role of director
  users = User.query.filter_by(role=UserRole.DIRECTOR).all()

  # Create a Director for each user
  directors = [create_director(user.id) for user in users]

  db.session.add_all(directors)
  db.session.commit()
