from app.models import Director, Movie
from app import db
from app.factories.movie_factory import create_movie

def seed_movies():
  directors = Director.query.all()
  movies = []

  for director in directors:
    # Create movies for each director
    for _ in range(3):
      movies.append(create_movie(director.id))

  db.session.add_all(movies)
  db.session.commit()
