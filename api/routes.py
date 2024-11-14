from flask import Blueprint, render_template, request, jsonify
from models import db, User
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from serializers.login_serializer import LoginSerializer
from serializers.verify_token_serializer import VerifyTokenSerializer

# Create a blueprint for your routes
main = Blueprint('main', __name__)

# Define your routes here
@main.route("/")  # Home route
def home():
    return "Method not auth", 405


@main.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    login_serializer = LoginSerializer(username, password)

    response, status_code = login_serializer.validate()

    return jsonify(response), status_code

@main.route("/verify_token", methods=["GET"])
@jwt_required()
def verify_token():
    current_user = get_jwt_identity()

    verify_token_serializer = VerifyTokenSerializer(current_user)

    response, status_code = verify_token_serializer.validate()

    return jsonify(response), status_code

# Route to fetch all users
@main.route("/users")
def get_users():
    users = User.query.all()  # Query all users from the database
    return {"users": [{"id": u.id, "username": u.username} for u in users]}
