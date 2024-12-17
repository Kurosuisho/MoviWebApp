from flask import Flask
from datamanager.SQLiteDataManager import SQLiteDataManager
import os

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
    return str([user.name for user in users])  # Return user names as a list

if __name__ == '__main__':
    app.run(debug=True)
    