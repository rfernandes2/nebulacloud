from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Primary Key
    username = db.Column(db.String(80), unique=True, nullable=False)  # Unique Username
    password = db.Column(db.String(200), nullable=False)  # Password (hashed)

    def __repr__(self):
        return f"<User {self.username}>"
