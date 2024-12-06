# Database models # Database models

from extensions import db

class Book(db.Model):
    """
    Book model for the database.
    """
    id = db.Column(db.Integer, primary_key=True)  # Primary key
    title = db.Column(db.String(120), nullable=False)  # Title of the book
    author = db.Column(db.String(120), nullable=False)  # Author of the book

    def __repr__(self):
        return f'<Book {self.title}>'


class User(db.Model):
    """
    User model for the database.
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)  # Store hashed passwords

    def __repr__(self):
        return f'<User {self.username}>'




