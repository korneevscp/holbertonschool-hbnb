from flask_restx import Namespace, Resource, fields
from app.services.facade import HBnBFacade

api = Namespace('users', description='User operations')

# Define the user model for input validation and documentation
user_model = api.model('User', {
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user')
    'password': fields.String(required=True, description='Password for the user')
})

facade = HBnBFacade()

@api.route('/')
class UserList(Resource):
    @api.expect(user_model, validate=True)
    @api.response(201, 'User successfully created')
    @api.response(400, 'Email already registered')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new user"""
        user_data = api.payload

        # Simulate email uniqueness check (to be replaced by real validation with persistence)
        existing_user = facade.get_user_by_email(user_data['email'])
        if existing_user:
            return {'error': 'Email already registered'}, 400

        hashed_password = generate_password_hash(user_data['password'])

        # Create a new user with the hashed password
        user_data['password'] = hashed_password

        new_user = facade.create_user(user_data)
        return {'id': new_user.id, 'first_name': new_user.first_name, 'last_name': new_user.last_name, 'email': new_user.email}, 201

class HBnBFacade:
    def create_user(self, user_data):
        # Création de l'utilisateur dans la base de données
        # Assurez-vous que le mot de passe est stocké sous forme hachée
        new_user = User(
            first_name=user_data['first_name'],
            last_name=user_data['last_name'],
            email=user_data['email'],
            password=user_data['password']  # Le mot de passe est déjà haché ici
        )
        db.session.add(new_user)
        db.session.commit()
        return new_user

@api.route('/<owner_id>')
class UserResource(Resource):
    @api.response(200, 'User details retrieved successfully')
    @api.response(404, 'User not found')
    def get(self, owner_id):
        """Get user details by ID"""
        user = facade.get_user(owner_id)
        if not user:
            return {'error': 'User not found'}, 404
         user_data = {
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email
        }

        return user_data, 200
