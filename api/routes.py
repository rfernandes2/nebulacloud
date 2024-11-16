from flask import Blueprint, render_template, request, jsonify
from api.models import db, User
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from api.serializers.login_serializers import LoginSerializer
from api.serializers.verify_token_serializer import VerifyTokenSerializer
from api.serializers.list_serializers import ListSerializers

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

@main.route("/list", methods=["GET"])
@jwt_required()
def list_dir():
    current_user = get_jwt_identity()
    data = request.get_json(silent=True)

    if not data:
        data = None

    list_serializer = ListSerializers(current_user, data['path'])
    return list_serializer.list()

# Route to fetch all users
@main.route("/users")
@jwt_required()
def get_users():
    users = User.query.all()  # Query all users from the database
    return {"users": [{"id": u.id, "username": u.username} for u in users]}
