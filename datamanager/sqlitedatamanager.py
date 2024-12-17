
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from MoviWeb_APP.datamanager.data_manager_interface import DataManagerInterface

# Defining database models
Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    movies = relationship("Movie", back_populates="user")


class Movie(Base):
    __tablename__ = 'movies'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    director = Column(String, nullable=False)
    year = Column(Integer, nullable=False)
    rating = Column(Integer, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("User", back_populates="movies")


class SQLiteDataManager(DataManagerInterface):

    def __init__(self, user_movie_database):
        """Initialize the SQLite database and session."""
        self.engine = create_engine(f'sqlite:///data/{user_movie_database}.sqlite')
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()

    def get_all_users(self):
        """Fetch a list of all users."""
        return self.session.query(User).all()

    def get_user_movies(self, user_id):
        """Retrieve all movies for a specific user."""
        user = self.session.query(User).filter_by(id=user_id).first()
        if user:
            return user.movies
        return []

    def add_user(self, name):
        """Add a new user to the database."""
        new_user = User(name=name)
        self.session.add(new_user)
        self.session.commit()
        return new_user

    def add_movie(self, user_id, name, director, year, rating):
        """Add a new movie for a specific user."""
        user = self.session.query(User).filter_by(id=user_id).first()
        if user:
            new_movie = Movie(
                name=name, director=director, year=year, rating=rating, user=user
            )
            self.session.add(new_movie)
            self.session.commit()
            return new_movie
        raise ValueError("User not found")

    def update_movie(self, movie_id, name, director, year, rating):
        """Modify details of a specific movie."""
        movie = self.session.query(Movie).filter_by(id=movie_id).first()
        if movie:
            movie.name = name
            movie.director = director
            movie.year = year
            movie.rating = rating
            self.session.commit()
            return movie
        raise ValueError("Movie not found")

    def delete_movie(self, movie_id):
        """Delete a specific movie."""
        movie = self.session.query(Movie).filter_by(id=movie_id).first()
        if movie:
            self.session.delete(movie)
            self.session.commit()
            return True
        raise ValueError("Movie not found")
