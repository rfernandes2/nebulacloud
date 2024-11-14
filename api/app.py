from flask import Flask
from flask_jwt_extended import JWTManager
from routes import main  # Import the blueprint
from settings import sql_url, sql_track_mod, jwt_key
from models import db  # Ensure you import `db` only once from models

app = Flask(__name__)

# Register the blueprint
app.register_blueprint(main)

# Configure your app's database or other settings
app.config['SQLALCHEMY_DATABASE_URI'] = sql_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = sql_track_mod
app.config['JWT_SECRET_KEY'] = jwt_key  # Ensure you replace this with a secure key

# Initialize the app with the db and Initialize JWTManager
db.init_app(app)
jwt = JWTManager(app)

# Check if the database exists, and create tables if not
with app.app_context():
    # This will create the tables if they don't already exist
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)
