from flask import Blueprint, render_template, jsonify
from models import db, User

# Create a blueprint for your routes
main = Blueprint('main', __name__)

# Define your routes here
@main.route("/")  # Home route
def home():
    return 'Method not allowed', 405

# List users
@main.route("/users", methods=["GET"])
def list_users():
    users = User.query.all()
    return jsonify({"users": [{"id": user.id, "username": user.username} for user in users]}), 200
