import bcrypt
from flask_jwt_extended import create_access_token
from datetime import timedelta
from api.models import User

class LoginSerializer:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def authenticate_user(self):
        user = User.query.filter_by(username=self.username).first()
        # Check if user exists and the provided password matches the stored hashed password
        if user and bcrypt.checkpw(self.password.encode('utf-8'), user.password.encode('utf-8')):
            return user
        return None

    def generate_token(self):
        # Gera o token JWT
        return create_access_token(identity=self.username, expires_delta=timedelta(minutes=60))

    def validate(self):
        user = self.authenticate_user()
        if user:
            access_token = self.generate_token()
            return {"access_token": access_token}, 200
        else:
            return {"msg": "Invalid username or password"}, 401
