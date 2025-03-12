from flask_restx import Namespace, Resource, fields
from flask import request
from app.services.facade import HBnBFacade
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt

api = Namespace('users', description='User operations')
facade = HBnBFacade()

# Modèle utilisateur pour validation des mises à jour
user_update_model = api.model('UserUpdate', {
    'first_name': fields.String(description="User's first name"),
    'last_name': fields.String(description="User's last name"),
    'email': fields.String(description="User's email"),
    'password': fields.String(description="User's password")
})

# Modèle admin pour création d'utilisateur
admin_user_create_model = api.model('AdminUserCreate', {
    'first_name': fields.String(required=True, description="User's first name"),
    'last_name': fields.String(required=True, description="User's last name"),
    'email': fields.String(required=True, description="User's email"),
    'password': fields.String(required=True, description="User's password"),
    'is_admin': fields.Boolean(description="Admin status", default=False)
})

@api.route('/')
class UserList(Resource):
    @api.expect(user_update_model, validate=True)
    @api.response(201, 'User successfully created')
    @api.response(400, 'Email already registered')
    def post(self):
        """Register a new user"""
        user_data = api.payload
        # Vérifier si l'email existe déjà
        existing_user = facade.get_user_by_email(user_data['email'])
        if existing_user:
            return {'error': 'Email already registered'}, 400
        # Créer l'utilisateur avec hachage du mot de passe
        new_user = facade.create_user({
            'first_name': user_data['first_name'],
            'last_name': user_data['last_name'],
            'email': user_data['email'],
            'password': user_data['password']  # Facade doit gérer le hachage
        })
        return {'id': new_user.id, 'message': 'User successfully created'}, 201

@api.route('/admin')
class AdminUserCreate(Resource):
    @jwt_required()
    @api.expect(admin_user_create_model, validate=True)
    @api.response(201, 'User successfully created by admin')
    @api.response(400, 'Email already registered')
    @api.response(403, 'Admin privileges required')
    def post(self):
        """Create a new user (admin only)"""
        # Vérifier si l'utilisateur est admin
        claims = get_jwt()
        if not claims.get('is_admin'):
            return {'error': 'Admin privileges required'}, 403
            
        user_data = api.payload
        
        # Vérifier si l'email existe déjà
        existing_user = facade.get_user_by_email(user_data['email'])
        if existing_user:
            return {'error': 'Email already registered'}, 400
            
        # Créer l'utilisateur avec les données fournies
        new_user = facade.create_user({
            'first_name': user_data['first_name'],
            'last_name': user_data['last_name'],
            'email': user_data['email'],
            'password': user_data['password'],
            'is_admin': user_data.get('is_admin', False)
        })
        
        return {'id': new_user.id, 'message': 'User successfully created by admin'}, 201

@api.route('/<user_id>')
class UserResource(Resource):
    @api.response(200, 'User details retrieved successfully')
    @api.response(404, 'User not found')
    def get(self, user_id):
        """Get user details by ID (without password)"""
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        return {
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email
        }, 200

    @jwt_required()  # Assurez-vous que l'utilisateur est authentifié
    @api.expect(user_update_model, validate=True)
    @api.response(200, 'User updated successfully')
    @api.response(403, 'Forbidden: You can only edit your own information')
    @api.response(400, 'You cannot modify the email or password')
    @api.response(404, 'User not found')
    def put(self, user_id):
        """Update user information (only first name and last name)"""
        # Récupérer l'utilisateur actuel (obtenu depuis le token JWT)
        current_user_id = get_jwt_identity()
        # Vérifier que l'utilisateur authentifié correspond à l'utilisateur que l'on tente de modifier
        if current_user_id != user_id:
            return {'error': 'Forbidden: You can only edit your own information'}, 403
        # Vérifier si l'utilisateur existe
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        # Récupérer les données envoyées
        user_data = api.payload
        # Vérifier si l'email ou le mot de passe ont été modifiés
        if 'email' in user_data or 'password' in user_data:
            return {'error': 'You cannot modify the email or password'}, 400
        # Filtrer les champs autorisés (first_name, last_name)
        updated_data = {}
        if 'first_name' in user_data:
            updated_data['first_name'] = user_data['first_name']
        if 'last_name' in user_data:
            updated_data['last_name'] = user_data['last_name']
        # Mise à jour des informations de l'utilisateur
        facade.update_user(user_id, updated_data)
        return {'message': 'User updated successfully'}, 200
