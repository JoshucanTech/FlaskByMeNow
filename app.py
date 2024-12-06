# Entry point # Entry point
from flask import Flask, request
from config import Config
from extensions import db, ma
from routes import api
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
import logging



def create_app():
    """
    Application factory function.
    """
    app = Flask(__name__)
    app.config.from_object(Config)  # Load configuration
    jwt = JWTManager(app)  # Initialize JWT manager


    # Initialize extensions
    db.init_app(app)
    ma.init_app(app)
    

    # Initialize Flask-Migrate
    migrate = Migrate(app, db)  # Pass app and db to Migrate

    # Setup logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    # # Log request details before handling each request
    # @app.before_request
    # def log_request_info():
    #     """
    #     Log request details.
    #     """
    #     logger.info(f"Request: {request.method} {request.url} - {request.data}")

    # Register blueprints
    app.register_blueprint(api, url_prefix='/api')

    return app

# Run the app
if __name__ == '__main__':
    app = create_app()
    app.run()
