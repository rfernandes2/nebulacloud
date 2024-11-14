from flask import Flask
from models import db, User  # Import the db and User model

# Initialize Flask app
app = Flask(__name__)

# Configure SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
db.init_app(app)

# Create tables (run once)
with app.app_context():
    db.create_all()
    print("Database and tables created successfully!")

if __name__ == "__main__":
    app.run(debug=True)
