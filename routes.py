# API routes # API routes


from flask import Blueprint, request, jsonify
from extensions import db
from models import Book, User
from marshmallow import Schema, fields
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash


# Blueprint for API routes
api = Blueprint('api', __name__)

# Schema for validation and serialization
class BookSchema(Schema):
    id = fields.Int(dump_only=True)  # Read-only ID
    title = fields.Str(required=True)  # Title (required)
    author = fields.Str(required=True)  # Author (required)

# Create schema instances
book_schema = BookSchema()  # Single book schema
books_schema = BookSchema(many=True)  # Multiple books schema


# Get all books by authenticated user
@api.route('/books/all', methods=['GET'])
@jwt_required()  # Protect route
def get_all_books():
    """
    Fetch all books. Requires authentication.
    """
    books = Book.query.all()  # Fetch all books
    return jsonify(books_schema.dump(books)), 200



# Get all books
@api.route('/books', methods=['GET'])
def get_books():
    """
    Fetch all books from the database.
    """
    books = Book.query.all()  # Fetch all books
    return jsonify(books_schema.dump(books)), 200



@api.route('/books/paginated', methods=['GET'])
def get_books_paginated():
    """
    Fetch paginated books.
    """
    page = request.args.get('page', 1, type=int)  # Get page from query params
    per_page = request.args.get('per_page', 10, type=int)  # Items per page
    paginated_books = Book.query.paginate(page=page, per_page=per_page, error_out=False)
    
    return jsonify({
        "books": books_schema.dump(paginated_books.items),
        "total": paginated_books.total,
        "pages": paginated_books.pages,
        "current_page": paginated_books.page
    }), 200



# Get book by id
@api.route('/books/<int:book_id>', methods=['GET'])
def get_each_book(book_id):
    """
    Fetch a book from the database.
    """
    book = Book.query.get_or_404(book_id)  # Fetch all books
    return jsonify(book_schema.dump(book)), 200

# Add a new book
@api.route('/books', methods=['POST'])
def add_book():
    """
    Add a new book to the database.
    """
    data = request.get_json()
    errors = book_schema.validate(data)  # Validate input data
    if errors:
        return jsonify(errors), 400  # Return validation errors

    new_book = Book(**data)  # Create a new Book instance
    db.session.add(new_book)  # Add to session
    db.session.commit()  # Commit transaction
    return jsonify(book_schema.dump(new_book)), 201

# Update a book
@api.route('/books/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    """
    Update an existing book by ID.
    """
    book = Book.query.get_or_404(book_id)  # Fetch book or return 404
    data = request.get_json()
    errors = book_schema.validate(data, partial=True)  # Partial validation for updates
    if errors:
        return jsonify(errors), 400

    for key, value in data.items():
        setattr(book, key, value)  # Update attributes
    db.session.commit()  # Commit transaction
    return jsonify(book_schema.dump(book)), 200

# Delete a book
@api.route('/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    """
    Delete a book by ID.
    """
    book = Book.query.get_or_404(book_id)  # Fetch book or return 404
    db.session.delete(book)  # Mark book for deletion
    db.session.commit()  # Commit transaction
    return jsonify({"message": "Book deleted"}), 200


# User registration
@api.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    hashed_password = generate_password_hash(data.get('password'))
    new_user = User(username=data.get('username'), password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User registered"}), 201




# Login Route
@api.route('/login', methods=['POST'])
def login():
    """
    Authenticate user and return a JWT.
    """
    # Check if the request contains valid JSON
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Missing JSON data"}), 400
    except Exception as e:
        return jsonify({"error": f"Invalid JSON: {str(e)}"}), 400

    # Validate presence of required fields
    if 'username' not in data or 'password' not in data:
        return jsonify({"error": "Missing 'username' or 'password'"}), 400

    # Authenticate user
    user = User.query.filter_by(username=data['username']).first()
    if not user or not check_password_hash(user.password, data['password']):
        return jsonify({"error": "Invalid username or password"}), 401

    # Generate JWT token
    access_token = create_access_token(identity=str(user.id))
    return jsonify({"access_token": access_token}), 200



# Protected route example
@api.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user = get_jwt_identity()  # Get current user's identity
    return jsonify(logged_in_as=current_user), 200
