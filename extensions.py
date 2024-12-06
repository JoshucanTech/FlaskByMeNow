# Flask extensions # Flask extensions

from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager





# Initialize Flask extensions
db = SQLAlchemy()  # SQLAlchemy for ORM
ma = Marshmallow()  # Marshmallow for serialization/validation
