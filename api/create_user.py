from app import app
from api.models import db, User
import bcrypt

with app.app_context():
    username = input('Enter username: ')
    password = input('Enter password: ')

    existing_user = User.query.filter_by(username=username).first()

    if existing_user:
        print(f"ERROR: User {username} already exists!")
    else:
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        # Create a new user instance with the hashed password
        new_user = User(username=username, password=hashed_password.decode('utf-8'), path=username)
        db.session.add(new_user)
        db.session.commit()

        print(f"SUCCESS: User {username} created successfully!")