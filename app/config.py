import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL', f'sqlite:///{os.path.join(BASE_DIR, "db.sqlite3")}')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_USER_TOKEN = os.getenv('JWT_USER_TOKEN', 'auth_token')