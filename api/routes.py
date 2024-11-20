from flask import Blueprint, render_template, request, jsonify
from api.models import db, User
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from api.serializers.login_serializers import LoginSerializer
from api.serializers.verify_token_serializer import VerifyTokenSerializer
from api.serializers.list_serializers import ListSerializers
import bcrypt

# Create a blueprint for your routes
main = Blueprint('main', __name__)

# Define your routes here
@main.route("/")  # Home route
def home():
    return "Method not auth", 405

@main.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if User.query.filter_by(username=username).first():
        return jsonify({"error": "User already exists"}), 400

    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    new_user = User(username=username, password=hashed_password.decode('utf-8'), path=username)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"success": f"User {username} created successfully!"}), 201

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

@main.route("/list", methods=["POST"])
@jwt_required()
def list_dir():
    current_user = get_jwt_identity()
    data = request.get_json(silent=True) or {}

    # If no `path` is provided, default to None
    path = data.get('path', None)

    list_serializer = ListSerializers(current_user, path)
    return list_serializer.list()

@main.route("/create_folder", methods=["POST"])
@jwt_required()
def create_folder():
    current_user = get_jwt_identity()
    data = request.get_json()

    if data and 'path' in data:
        if 'folder_name' in data:
            path = data['path']
            folder_name = data['folder_name']
            list_serializer = ListSerializers(current_user, path)
            return list_serializer.create_folder(folder_name)
        else:
            return jsonify({"error": "Missing folder name"}), 400
    else:
        return jsonify({"error": "Missing path"}), 400

@main.route("/delete", methods=["DELETE"])
@jwt_required()
def delete_item():
    current_user = get_jwt_identity()
    data = request.get_json()

    if data and 'path' in data:
        path = data['path']
        list_serializer = ListSerializers(current_user, path)
        return list_serializer.delete_item()
    else:
        return jsonify({"error": "Missing 'path' in request data"}), 400

# Route to fetch all users
@main.route("/users")
@jwt_required()
def get_users():
    users = User.query.all()  # Query all users from the database
    return {"users": [{"id": u.id, "username": u.username} for u in users]}

@main.route("/upload", methods=["POST"])
@jwt_required()
def upload_files():
    current_user = get_jwt_identity()
    data = request.form  # Form data, as file is uploaded via form

    path = data.get('path', None)
    files = request.files.getlist('file')  # Get multiple files from the request

    if not files:
        return jsonify({"error": "No files provided"}), 400

    if not path:
        return jsonify({"error": "No path provided"}), 400

    # Create the ListSerializers instance and upload the files
    list_serializer = ListSerializers(current_user, path)
    return list_serializer.upload_files(files)

@main.route('/download', methods=['GET'])
@jwt_required()
def download_file():
    current_user = get_jwt_identity()
    path = request.args.get('path')

    if not path:
        return jsonify({'error': 'No path provided'}), 400
    
    list_serializer = ListSerializers(current_user, path)
    return list_serializer.download_file()