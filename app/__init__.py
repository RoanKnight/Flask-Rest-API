from flask import Flask
from .extensions import db, migrate, ma, jwt
# from .routes.user_routes import user_routes

def create_app():
  app = Flask(__name__)
  app.config.from_object('app.config.Config')

  db.init_app(app)
  migrate.init_app(app, db)
  ma.init_app(app)
  jwt.init_app(app)

  # user_routes(app)

  return app
