from flask import Blueprint, render_template
from models import db, User

# Create a blueprint for your routes
main = Blueprint('main', __name__)

# Define your routes here
@main.route("/")  # Home route
def home():
    return "Welcome to your Flask app!"

@main.route("/about")  # About route
def about():
    return "This is the About page!"

# Route to fetch all users
@main.route("/users")
def get_users():
    users = User.query.all()  # Query all users from the database
    return {"users": [{"id": u.id, "username": u.username} for u in users]}
