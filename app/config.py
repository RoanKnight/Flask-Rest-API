import os
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

# Configuration class for the Flask application
class Config:
  # Base directory of the application
  BASE_DIR = os.path.abspath(os.path.dirname(__file__))

  # Database URI
  SQLALCHEMY_DATABASE_URI = os.getenv(
      'DATABASE_URL', f'sqlite:///{os.path.join(BASE_DIR, "db.sqlite3")}')

  # Disable SQLAlchemy event system to save resources
  SQLALCHEMY_TRACK_MODIFICATIONS = False

  # JWT token for user authentication,
  JWT_USER_TOKEN = os.getenv('JWT_USER_TOKEN', 'auth_token')
