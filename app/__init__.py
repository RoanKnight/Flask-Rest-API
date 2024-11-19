from flask import Flask
from .extensions import db, migrate, ma, jwt
from .models import User, UserRole, Director, Customer
from .routes.user_routes import user_routes
from .routes.auth_routes import auth_routes
from .routes.customer_routes import customer_routes

def create_app():
  app = Flask(__name__)
  app.config.from_object('app.config.Config')
  app.json.sort_keys = False

  # Initialize extensions
  db.init_app(app)
  migrate.init_app(app, db)
  ma.init_app(app)
  jwt.init_app(app)

  # Register blueprints
  app.register_blueprint(auth_routes)
  app.register_blueprint(user_routes, url_prefix='/api')
  app.register_blueprint(customer_routes, url_prefix='/api')

  return app
