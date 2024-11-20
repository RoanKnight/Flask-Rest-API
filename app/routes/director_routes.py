from flask import Blueprint, request, jsonify
from app import db
from app.models import UserRole, Director, Movie
from app.schemas.director_schema import DirectorSchema
from app.schemas.movie_schema import MovieSchema
from app.middleware import token_required, role_required

director_routes = Blueprint('director_routes', __name__)
director_schema = DirectorSchema()
movie_schema = MovieSchema()

@director_routes.route('/directors', methods=['GET'])
@token_required
@role_required(UserRole.DIRECTOR)
def index(current_user):
  directors = Director.query.all()
  directors_data = director_schema.dump(directors, many=True)
  response = {
      "success": {
          "directors": directors_data
      }
  }
  return jsonify(response), 200

@director_routes.route('/directors/<int:id>', methods=['GET'])
@token_required
@role_required(UserRole.DIRECTOR)
def show(current_user, id):
  director = Director.query.get(id)
  if not director:
    return jsonify({"message": "Director not found"}), 404

  director_data = director_schema.dump(director)
  response = {
      "success": {
          "director": director_data
      }
  }
  return jsonify(response), 200

@director_routes.route('/directors/showMovies', methods=['GET'])
@token_required
@role_required(UserRole.DIRECTOR)
def show_movies(current_user):
  director = Director.query.filter_by(user_id=current_user.id).first()
  if not director:
    return jsonify({"message": "Director not found"}), 404

  # Get all movies for the director
  movies = Movie.query.filter_by(director_id=director.id).all()

  # Serialize the movie details
  movies_data = movie_schema.dump(movies, many=True)

  response = {
      "success": {
          "movies": movies_data
      }
  }
  return jsonify(response), 200

@director_routes.route('/directors/updateDirector', methods=['PUT'])
@token_required
@role_required(UserRole.DIRECTOR)
def update_director(current_user):
  data = request.get_json()
  if not data:
    return jsonify({"message": "No input data provided"}), 400

  director = Director.query.filter_by(user_id=current_user.id).first()
  if not director:
    return jsonify({"message": "Director not found"}), 404

  website_url = data.get('website_url')
  if website_url:
    director.website_url = website_url

  db.session.commit()
  director_data = director_schema.dump(director)
  response = {
      "success": {
          "director": director_data
      }
  }
  return jsonify(response), 200
