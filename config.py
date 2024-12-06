# Configuration settings # Configuration settings

import os

class Config:
    """
    Base configuration class with default settings.
    """
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///books.db')  # Database URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Disable tracking for performance
    DEBUG = True  # Enable debug mode
    # JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'your_secret_key')  # Change to a secure key
    JWT_SECRET_KEY = 'your_secret_key'  # Change to a secure key

