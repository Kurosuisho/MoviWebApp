
from flask_sqlalchemy import SQLAlchemy
from datamanager.DataManagerInterface import DataManagerInterface
from datamanager.data_models import User, Movie

class SQLiteDataManager:
    def __init__(self):
        self.db = SQLAlchemy()

    def init_app(self, app):
        self.db.init_app(app)
        
    def get_all_users(self):
        """Retrieve all users from the database."""
        users = User.query.all()
        return users

    def get_user_movies(self, user_id):
        """Retrieve all movies for a given user."""
        movies = Movie.query.filter_by(user_id=user_id).all()
        return movies

    def add_user(self, name):
        """Add a new user to the database."""
        new_user = User(name=name)
        self.db.session.add(new_user)
        self.db.session.commit()
        return new_user

    def add_movie(self, user_id, name, director, year, rating):
        """Add a new movie to the database."""
        new_movie = Movie(user_id=user_id, name=name, director=director, year=year, rating=rating)
        self.db.session.add(new_movie)
        self.db.session.commit()
        return new_movie

    def update_movie(self, movie_id, name=None, director=None, year=None, rating=None):
        """Update details of a specific movie."""
        movie = Movie.query.get(movie_id)
        if not movie:
            return None
        if name is not None:
            movie.name = name
        if director is not None:
            movie.director = director
        if year is not None:
            movie.year = year
        if rating is not None:
            movie.rating = rating
        self.db.session.commit()
        return movie

    def delete_movie(self, movie_id):
        """Delete a specific movie from the database."""
        movie = Movie.query.get(movie_id)
        if not movie:
            return None
        self.db.session.delete(movie)
        self.db.session.commit()
        return movie
    
    