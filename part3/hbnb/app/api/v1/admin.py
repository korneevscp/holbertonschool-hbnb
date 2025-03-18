from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from part3.hbnb.app.services import facade
from flask import request

api = Namespace('admin', description='Admin operations')

user_model = api.model('User', {
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user'),
    'is_admin': fields.Boolean(required=True, description='Whether the user is an admin'),
    'password': fields.String(required=True, description='Password of the user')
})

amenity_model = api.model('Amenity', {
    'name': fields.String(required=True, description='Name of the amenity')
})


@api.route('/users/')
class AdminUserCreate(Resource):
    @jwt_required()
    @api.expect(user_model, validate=True)
    @api.response(201, 'User successfully created')
    @api.response(400, 'Email already registered')
    @api.response(400, 'Invalid input data')
    def post(self):
        current_user = get_jwt_identity()

        if not current_user.get('is_admin'):
            return {'error': 'Admin privileges required'}, 403

        user_data = request.json
        email = user_data.get('email')

        # Check if email is already in use
        if facade.get_user_by_email(email):
            return {'error': 'Email already registered'}, 400

        # Logic to create a new user
        new_user = facade.create_user(user_data)
        return {'id': new_user.id,
                'first_name': new_user.first_name,
                'last_name': new_user.last_name,
                'email': new_user.email,
                'is_admin': new_user.is_admin}, 201


@api.route('/users/<user_id>')
class AdminUserResource(Resource):
    @jwt_required()
    @api.response(200, 'User updated successfully')
    @api.response(404, 'User not found')
    def put(self, user_id):
        current_user = get_jwt_identity()

        # If 'is_admin' is part of the identity payload
        if not current_user.get('is_admin'):
            return {'error': 'Admin privileges required'}, 403

        user_data = request.json
        email = user_data.get('email')

        if email:
            # Check if email is already in use
            existing_user = facade.get_user_by_email(email)
            if existing_user and existing_user.id != user_id:
                return {'error': 'Email is already in use'}, 400

        # Logic to update user details
        updated_user = facade.update_user(user_id, user_data)
        if not updated_user:
            return {'error': 'User not found'}, 404
        return {'id': updated_user.id,
                'first_name': updated_user.first_name,
                'last_name': updated_user.last_name,
                'email': updated_user.email}, 200


@api.route('/amenities/')
class AdminAmenityCreate(Resource):
    # @jwt_required()
    @api.response(201, 'Amenity successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        # current_user = get_jwt_identity()

        #  if not current_user.get('is_admin'):
        #  return {'error': 'Admin privileges required'}, 403

        # Logic to create a new amenity
        try:
            new_amenity = facade.create_amenity(request.json)
            return {
                'id': new_amenity.id,
                'name': new_amenity.name
            }, 201
        except Exception as e:
            api.abort(400, str(e))


@api.route('/amenities/<amenity_id>')
class AdminAmenityModify(Resource):
    @jwt_required()
    @api.response(200, 'Amenity details retrieved successfully')
    @api.response(404, 'Amenity not found')
    def put(self, amenity_id):
        current_user = get_jwt_identity()

        if not current_user.get('is_admin'):
            return {'error': 'Admin privileges required'}, 403

        # Logic to update an amenity
        try:
            updated_amenity = facade.update_amenity(amenity_id, request.json)
            if updated_amenity:
                return {
                    'id': updated_amenity.id,
                    'name': updated_amenity.name
                }, 200
            else:
                api.abort(404, 'Amenity not found')
        except Exception as e:
            api.abort(400, str(e))


@api.route('/places/<place_id>')
class AdminPlaceModify(Resource):
    @jwt_required()
    @api.response(200, 'Place details retrieved successfully')
    @api.response(404, 'Place not found')
    def put(self, place_id):
        current_user = get_jwt_identity()

        # Set is_admin default to False if not exists
        is_admin = current_user.get('is_admin', False)
        user_id = current_user.get('id')

        place = facade.get_place(place_id)
        if not is_admin and place.owner_id != user_id:
            return {'error': 'Unauthorized action'}, 403

        # Logic to update the place
        updated_place = facade.update_place(place_id, request.json)
        return {
            'id': updated_place.id,
            'title': updated_place.title,
            'description': updated_place.description,
            'price': updated_place.price
        }, 200
