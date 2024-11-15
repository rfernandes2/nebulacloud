from flask import Blueprint, render_template, request, jsonify
from api.models import db, User
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from api.serializers.login_serializers import LoginSerializer
from api.serializers.verify_token_serializer import VerifyTokenSerializer
from api.settings import default_path
import os

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
    user_dir = f"{default_path}{current_user}"

    if not os.path.exists(user_dir):
        return jsonify({"error": "User directory does not exist"}), 404

    try:
        folders = {}

        for folder_name in os.listdir(user_dir):
            folder_path = os.path.join(user_dir, folder_name)

            if os.path.isdir(folder_path):  # If it's a directory
                # List files and subfolders within the directory
                subfiles = []
                subfolders = []
                for subfolder_name in os.listdir(folder_path):
                    subfolder_path = os.path.join(folder_path, subfolder_name)
                    if os.path.isdir(subfolder_path):
                        subfolders.append(subfolder_name)
                    elif os.path.isfile(subfolder_path):
                        subfiles.append(subfolder_name)

                # Add the folder's contents to the dictionary
                folders[folder_name] = {
                    "files": subfiles,
                    "folders": subfolders
                }

        return jsonify({
            "folders": folders
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Route to fetch all users
@main.route("/users")
@jwt_required()
def get_users():
    users = User.query.all()  # Query all users from the database
    return {"users": [{"id": u.id, "username": u.username} for u in users]}
