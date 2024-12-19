from flask import Flask, render_template, request, redirect
from datamanager.SQLiteDataManager import SQLiteDataManager
from dotenv import load_dotenv
import os
import requests

# Load environment variables from .env file
load_dotenv()

# Get the API key from the environment variable
OMDB_API_KEY = os.getenv('OMDB_API_KEY')

app = Flask(__name__)

# Create data directory if it doesn't exist
data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
os.makedirs(data_dir, exist_ok=True)

app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(data_dir, 'user_movie_database.sqlite')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

data_manager = SQLiteDataManager()
data_manager.init_app(app)

print(OMDB_API_KEY)  # Add this line temporarily to check if the key is loaded


@app.route('/')
def home():
    return "Welcome to MovieWeb App!"

@app.route('/users')
def list_users():
    try:
        users = data_manager.get_all_users()
        return render_template('users.html', users=users)
    except Exception as e:
        return f"An error occurred: {e}", 500

@app.route('/users/<int:user_id>')
def user_movies(user_id):
    try:
        users = data_manager.get_all_users()
        user = next((u for u in users if u.id == user_id), None)
        
        if not user:
            return render_template('404.html', message="User not found"), 404
        
        movies = data_manager.get_user_movies(user_id)
        return render_template('user_movies.html', user=user, movies=movies)
    except Exception as e:
        return f"An error occurred: {e}", 500

@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    try:
        if request.method == 'POST':
            name = request.form['name']
            data_manager.add_user(name)
            return redirect('/users')
        return render_template('add_user.html')
    except Exception as e:
        return f"An error occurred: {e}", 500

@app.route('/users/<int:user_id>/add_movie', methods=['GET', 'POST'])
def add_movie(user_id):
    try:
        if request.method == 'POST':
            movie_title = request.form['movie']
            
            # Fetch the movie details from OMDb API
            response = requests.get(f"http://www.omdbapi.com/?t={movie_title}&apikey={OMDB_API_KEY}")
            if response.status_code != 200:
                return f"Failed to fetch data from OMDb API. Status code: {response.status_code}", 500
            movie_data = response.json()
            
            # Add the movie to the database
            data_manager.add_movie(
                user_id=user_id,
                name=movie_data.get('Title', movie_title),
                director=movie_data.get('Director', 'Unknown'),
                year=movie_data.get('Year', 'Unknown'),
                rating=movie_data.get('imdbRating', 'N/A')
            )
            return redirect(f'/users/{user_id}')
        return render_template('add_movie.html', user_id=user_id)
    except Exception as e:
        return f"An error occurred: {e}", 500

@app.route('/users/<int:user_id>/update_movie/<int:movie_id>', methods=['GET', 'POST'])
def update_movie(user_id, movie_id):
    try:
        movies = data_manager.get_user_movies(user_id)
        movie_to_update = next((m for m in movies if m.id == movie_id), None)
        
        if not movie_to_update:
            return render_template('404.html', message="Movie not found"), 404

        if request.method == 'POST':
            name = request.form['name']
            director = request.form['director']
            year = request.form['year']
            rating = request.form['rating']

            data_manager.update_movie(
                movie_id=movie_id,
                name=name,
                director=director,
                year=year,
                rating=rating
            )
            return redirect(f'/users/{user_id}')
        return render_template('update_movie.html', user_id=user_id, movie=movie_to_update)
    except Exception as e:
        return f"An error occurred: {e}", 500

@app.route('/users/<int:user_id>/delete_movie/<int:movie_id>')
def delete_movie(user_id, movie_id):
    try:
        data_manager.delete_movie(movie_id)
        return redirect(f'/users/{user_id}')
    except Exception as e:
        return f"An error occurred: {e}", 500

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html', message="The page you are looking for does not exist"), 404

if __name__ == '__main__':
    app.run(debug=True)
