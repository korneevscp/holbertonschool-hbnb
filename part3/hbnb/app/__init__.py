from flask import Flask
from flask_restx import Api
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

bcrypt = Bcrypt()
jwt = JWTManager()
db = SQLAlchemy()

from part3.hbnb.app.api.v1.users import api as users_ns
from part3.hbnb.app.api.v1.places import api as places_ns
from part3.hbnb.app.api.v1.amenities import api as amenities_ns
from part3.hbnb.app.api.v1.reviews import api as reviews_ns
from part3.hbnb.app.api.v1.auth import api as auth_ns
from part3.hbnb.app.api.v1.admin import api as admin_ns
from part3.hbnb.app.api.v1.placeamenities import api as placeamenities_ns


def create_app(config_class="config.DevelopmentConfig"):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions with app context

    bcrypt.init_app(app)
    jwt.init_app(app)
    db.init_app(app)
    CORS(app)

    authorizations = {
        "BearerAuth": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header",
        }
    }

    api = Api(
        app,
        version='1.0',
        title='HBnB API',
        description='HBnB Application API',
        authorizations=authorizations,
        security="BearerAuth",
    )

    api.add_namespace(users_ns, path='/api/v1/users')
    api.add_namespace(places_ns, path='/api/v1/places')
    api.add_namespace(amenities_ns, path='/api/v1/amenities')
    api.add_namespace(reviews_ns, path='/api/v1/reviews')
    api.add_namespace(auth_ns, path='/api/v1/auth')
    api.add_namespace(admin_ns, path='/api/v1/admin')
    api.add_namespace(placeamenities_ns, path='/api/v1/placeamenities')

    return app
