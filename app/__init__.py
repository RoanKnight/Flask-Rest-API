from flask import Flask
from .extensions import db, migrate, ma, jwt, mail
from .models import User, UserRole, Director, Customer, Movie, CustomerMovie
from .routes.user_routes import user_routes
from .routes.auth_routes import auth_routes
from .routes.customer_routes import customer_routes
from .routes.director_routes import director_routes
from .routes.movie_routes import movie_routes
from .routes.customer_movie_routes import customer_movie_routes

def create_app():
  app = Flask(__name__)
  app.config.from_object('app.config.Config')
  # app.config['MAIL_SERVER']='localhost'
  # app.config['MAIL_PORT'] = 8025
  app.config['MAIL_SERVER']='sandbox.smtp.mailtrap.io'
  app.config['MAIL_PORT'] = 2525
  app.config['MAIL_USERNAME'] = '2121f4fd5722b2'
  app.config['MAIL_PASSWORD'] = '362e25189c10d9'
  app.config['MAIL_USE_TLS'] = True
  app.config['MAIL_USE_SSL'] = False
  app.config['MAIL_DEFAULT_SENDER'] = 'admin@movies.com'
  app.json.sort_keys = False

  # Initialize extensions
  db.init_app(app)
  migrate.init_app(app, db)
  ma.init_app(app)
  jwt.init_app(app)
  mail.init_app(app)

  # Register blueprints
  app.register_blueprint(auth_routes)
  app.register_blueprint(user_routes, url_prefix='/api')
  app.register_blueprint(customer_routes, url_prefix='/api')
  app.register_blueprint(director_routes, url_prefix='/api')
  app.register_blueprint(customer_movie_routes, url_prefix='/api')
  app.register_blueprint(movie_routes, url_prefix='/api')

  return app
