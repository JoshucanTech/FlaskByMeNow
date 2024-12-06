import pytest
from app import create_app
from extensions import db

@pytest.fixture
def app():
    """
    Create and configure a new app instance for testing.
    """
    test_app = create_app()
    test_app.config.update({
        "TESTING": True,  # Enable testing mode
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",  # In-memory DB for tests
        "JWT_SECRET_KEY": "test_secret",  # Test secret key
    })

    with test_app.app_context():
        db.create_all()  # Create tables
        yield test_app  # Provide the app instance
        db.drop_all()  # Cleanup

@pytest.fixture
def client(app):
    """
    Create a test client for the app.
    """
    return app.test_client()
