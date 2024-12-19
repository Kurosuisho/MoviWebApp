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


@app.route('/')
def home():
    return "Welcome to MovieWeb App!"


@app.route('/users')
def list_users():
    users = data_manager.get_all_users()
    return render_template('users.html', users=users)


@app.route('/users/<int:user_id>')
def user_movies(user_id):
    
    users = data_manager.get_all_users()
    user = None
    
    for u in users:
        if u.id == user_id:
            user = u
            break
        
    if not user:
        return "User not found", 404
    
    movies = data_manager.get_user_movies(user_id)
    return render_template('user_movies.html', user=user, movies=movies)


@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        name = request.form['name']
        data_manager.add_user(name)
        return redirect('/users')
    return render_template('add_user.html')



@app.route('/users/<int:user_id>/add_movie', methods=['GET', 'POST'])
def add_movie(user_id):
    if request.method == 'POST':
        # Get the movie title from the form using the "movie" key
        movie_title = request.form['movie']
        
        # Fetch the movie details from OMDb API
        response = requests.get(f"http://www.omdbapi.com/?t={movie_title}&apikey={OMDB_API_KEY}")
        movie_data = response.json()
        
        # Add the movie to the database using the fetched data
        data_manager.add_movie(
            user_id=user_id,
            name=movie_data.get('Title', movie_title),
            director=movie_data.get('Director', 'Unknown'),
            year=movie_data.get('Year', 'Unknown'),
            rating=movie_data.get('imdbRating', 'N/A')
        )
        return redirect(f'/users/{user_id}')
    
    return render_template('add_movie.html', user_id=user_id)



# @app.route('/users/<user_id>/update_movie/<movie_id>')
# def pass():
#     pass


# @app.route('/users/<user_id>/delete_movie/<movie_id>')
# def pass():
#     pass



if __name__ == '__main__':
    app.run(debug=True)