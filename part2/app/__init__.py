from flask import Flask
from flask_restx import Api
from app.api.v1.users import api as users_ns
from app.api.v1.amenities import api as amenities_ns
from app.api.v1.places import api as places_ns
from app.api.v1.reviews import api as reviews_ns
from flask_bcrypt import Bcrypt
from config import DevelopmentConfig
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy  # Importation manquante pour db

# Initialisation des extensions
db = SQLAlchemy()  # Création de l'instance db avant utilisation
bcrypt = Bcrypt()
jwt = JWTManager()

def create_app(config_class=DevelopmentConfig):  # Correction de l'import config
    app = Flask(__name__)  # Création de l'app avant utilisation
    
    # Configuration
    app.config.from_object(config_class)  # Ligne dupliquée corrigée
    
    # Initialisation des extensions avec l'app
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    
    # Initialisation de l'API
    api = Api(app, version='1.0', title='HBnB API', description='HBnB Application API')
    
    # Enregistrement des namespaces
    api.add_namespace(users_ns, path='/api/v1/users')
    api.add_namespace(amenities_ns, path='/api/v1/amenities')
    api.add_namespace(places_ns, path='/api/v1/places')
    api.add_namespace(reviews_ns, path='/api/v1/reviews')
    
    # Ajout du namespace auth pour l'authentification JWT
    from app.api.v1.auth import api as auth_ns
    api.add_namespace(auth_ns, path='/api/v1/auth')

    return app
