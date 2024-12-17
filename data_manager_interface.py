from abc import ABC, abstractmethod

class DataManagerInterface(ABC):

    @abstractmethod
    def get_all_users(self):
        """Retrieve a list of all users."""
        pass

    @abstractmethod
    def get_user_movies(self, user_id):
        """Retrieve all movies for a given user."""
        pass

    @abstractmethod
    def add_user(self, name):
        """Add a new user to the database."""
        pass

    @abstractmethod
    def add_movie(self, user_id, name, director, year, rating):
        """Add a new movie for a specific user."""
        pass

    @abstractmethod
    def update_movie(self, movie_id, name, director, year, rating):
        """Update details of a specific movie."""
        pass

    @abstractmethod
    def delete_movie(self, movie_id):
        """Delete a specific movie."""
        pass
