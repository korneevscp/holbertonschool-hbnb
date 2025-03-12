from flask_restx import Namespace, Resource, fields
from flask import request
from app.services.facade import HBnBFacade
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity

api = Namespace('users', description='User operations')
facade = HBnBFacade()

# Modèle utilisateur pour validation des mises à jour
user_update_model = api.model('UserUpdate', {
    'first_name': fields.String(description="User's first name"),
    'last_name': fields.String(description="User's last name"),
    'email': fields.String(description="User's email"),
    'password': fields.String(description="User's password")
})

def is_admin():
    """ Vérifie si l'utilisateur est administrateur """
    jwt_data = get_jwt()
    return jwt_data.get('role') == 'admin'

@api.route('/')
class UserList(Resource):
    @jwt_required()  # Authentification obligatoire
    @api.expect(user_update_model, validate=True)
    @api.response(201, 'User successfully created')
    @api.response(400, 'Email already registered')
    @api.response(403, 'Forbidden: Admins only')
    def post(self):
        """Register a new user (Admin only)"""
        if not is_admin():
            return {'error': 'Forbidden: Admins only'}, 403

        user_data = api.payload
        existing_user = facade.get_user_by_email(user_data['email'])
        if existing_user:
            return {'error': 'Email already registered'}, 400

        new_user = facade.create_user({
            'first_name': user_data['first_name'],
            'last_name': user_data['last_name'],
            'email': user_data['email'],
            'password': user_data['password']
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

    @jwt_required()
    @api.expect(user_update_model, validate=True)
    @api.response(200, 'User updated successfully')
    @api.response(403, 'Forbidden: Admins only')
    @api.response(400, 'You cannot modify the email or password')
    @api.response(404, 'User not found')
    def put(self, user_id):
        """Update user information (Admin only)"""
        if not is_admin():
            return {'error': 'Forbidden: Admins only'}, 403

        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404

        user_data = api.payload
        if 'email' in user_data or 'password' in user_data:
            return {'error': 'You cannot modify the email or password'}, 400

        updated_data = {}
        if 'first_name' in user_data:
            updated_data['first_name'] = user_data['first_name']
        if 'last_name' in user_data:
            updated_data['last_name'] = user_data['last_name']

        facade.update_user(user_id, updated_data)

        return {'message': 'User updated successfully'}, 200
