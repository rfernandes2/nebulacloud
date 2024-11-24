from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from api.routes import main  # Import the routes blueprint
from api.settings import sql_url, sql_track_mod, jwt_key
from api.models import db  # Ensure you import `db` only once from models

app = Flask(__name__)

# Enable CORS for only specific origins (more secure than allowing all origins)
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})

# Register the blueprint
app.register_blueprint(main)

# Configure the app's database or other settings
app.config['SQLALCHEMY_DATABASE_URI'] = sql_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = sql_track_mod
app.config['JWT_SECRET_KEY'] = jwt_key  # Ensure you replace this with a secure key

# Initialize the app with db and JWT
db.init_app(app)
jwt = JWTManager(app)

# Check if the database exists and create tables if not
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)
