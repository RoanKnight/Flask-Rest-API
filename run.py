from flask import Flask, redirect, url_for
from flask_cors import CORS
from flasgger import Swagger
from app.seeders.user_seeder import seed_users
from app.seeders.director_seeder import seed_directors
from app.seeders.customer_seeder import seed_customers
from app.seeders.movie_seeder import seed_movies
from app.seeders.customer_movie_seeder import seed_customer_movies
from app import create_app, db
import click
import os

# Create the Flask application
app = create_app()

# Enable CORS
CORS(app)

swagger = Swagger(app)

# Redirect the homepage to Swagger UI
@app.route('/')
def index():
  return redirect(url_for('flasgger.apidocs'))

# Command to seed the database
@app.cli.command("seed-database")
def seed_database():
  with app.app_context():
    db.drop_all()
    db.create_all()
    seed_users()
    seed_directors()
    seed_customers()
    seed_movies()
    seed_customer_movies()
    click.echo("Database refreshed and seeded successfully.")

# Command to drop all tables
@app.cli.command("drop-tables")
def drop_tables():
  with app.app_context():
    db.drop_all()
    click.echo("All tables dropped successfully.")

# Run the application
if __name__ == '__main__':
  app.run()
