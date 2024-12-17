from flask import Flask
from datamanager.SQLiteDataManager import SQLiteDataManager

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data/user_movie_database.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

data_manager = SQLiteDataManager()  # No argument passed here
data_manager.init_app(app)          # Link SQLiteDataManager to the Flask app



@app.route('/')
def home():
    return "Welcome to MovieWeb App!"


@app.route('/users')
def list_users():
    users = data_manager.get_all_users()
    return str(users)  # Temporarily returning users as a string

if __name__ == '__main__':
    app.run(debug=True)