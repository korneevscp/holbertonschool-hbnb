from flask_restx import Namespace, Resource, fields
from flask import request
from app.services.facade import HBnBFacade

api = Namespace('users', description='User operations')
facade = HBnBFacade()

# Modèle utilisateur pour validation
user_update_model = api.model('UserUpdate', {
    'first_name': fields.String(description="User's first name"),
    'last_name': fields.String(description="User's last name")
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

    @api.expect(user_update_model, validate=True)
    @api.response(200, 'User updated successfully')
    @api.response(403, 'Forbidden: You can only edit your own information')
    @api.response(404, 'User not found')
    def put(self, user_id):
        """Update user information (only first name and last name)"""
        user_data = api.payload
        if not user_data:
            return {'error': 'No input data'}, 400

        # Récupérer l'utilisateur actuel (simulation d'authentification avec un paramètre user_id)
        current_user_id = request.args.get('user_id')  # Supposons qu'on passe l'user_id en paramètre de requête
        if current_user_id != user_id:
            return {'error': 'Forbidden: You can only edit your own information'}, 403

        # Vérifier si l'utilisateur existe
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404

        # Modifier uniquement les champs autorisés
        updated_data = {}
        if 'first_name' in user_data:
            updated_data['first_name'] = user_data['first_name']
        if 'last_name' in user_data:
            updated_data['last_name'] = user_data['last_name']

        # Mise à jour des informations de l'utilisateur
        facade.update_user(user_id, updated_data)

        return {'message': 'User updated successfully'}, 200
