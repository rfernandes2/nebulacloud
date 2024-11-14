from app import app
from models import db, User


with app.app_context():
    username = input('Enter username: ')
    password = input('Enter password: ')

    existing_user = User.query.filter_by(username=username).first()

    if existing_user:
        print(f"ERROR: User {username} already exists!")
    else:
        new_user = User(username=username, password=password, path = username)
        db.session.add(new_user)
        db.session.commit()

        print(f"SUCCESS: User {username} created successfully!")