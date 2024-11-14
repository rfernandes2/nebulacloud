from flask import Flask
from routes import main  # Import the blueprint
from settings import sql_url, sql_track_mod

app = Flask(__name__)

# Register the blueprint
app.register_blueprint(main)

# Configure your app's database or other settings
app.config['SQLALCHEMY_DATABASE_URI'] = sql_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = sql_track_mod

# Initialize the app with the db
from models import db
db.init_app(app)

if __name__ == "__main__":
    app.run(debug=True)
