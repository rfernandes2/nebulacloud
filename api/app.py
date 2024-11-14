from flask import Flask
from routes import main  # Import the blueprint
from settings import sql_url, sql_track_mod
from models import db  # Import the db object

app = Flask(__name__)

# Register the blueprint
app.register_blueprint(main)

# Configure your app's database or other settings
app.config['SQLALCHEMY_DATABASE_URI'] = sql_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = sql_track_mod

# Initialize the app with the db
db.init_app(app)

# Check if the database exists, and create tables if not
with app.app_context():
    # This will create the tables if they don't already exist
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)
