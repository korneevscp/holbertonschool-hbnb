#!/usr/bin/python3
from flask_restx import Namespace, Resource, fields
from part3.hbnb.app.services import facade
from flask_jwt_extended import jwt_required, get_jwt_identity


api = Namespace('places', description='Place operations')

# Define the models for related entities
amenity_model = api.model('PlaceAmenity', {
    'id': fields.String(description='Amenity ID'),
    'name': fields.String(description='Name of the amenity')
})

user_model = api.model('PlaceUser', {
    'id': fields.String(description='User ID'),
    'first_name': fields.String(description='First name of the owner'),
    'last_name': fields.String(description='Last name of the owner'),
    'email': fields.String(description='Email of the owner')
})

# Added friday 15:

review_model = api.model('PlaceReview', {
    'id': fields.String(description='Review ID'),
    'text': fields.String(description='Text of the review'),
    'rating': fields.Integer(description='Rating of the place (1-5)'),
    'user_id': fields.String(description='ID of the user')
})

# Define the place model for input validation and documentation
place_model = api.model('Place', {
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude of the place'),
    'longitude': fields.Float(required=True, description='Longitude of the place'),
    'owner_id': fields.String(required=True, description='ID of the owner'),
    'amenities': fields.List(fields.String, required=True, description="List of amenities ID's")  # friday 15
})

create_place_model = api.model('PlaceCreate', {
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude of the place'),
    'longitude': fields.Float(required=True, description='Longitude of the place'),
    'owner_id': fields.String(required=True, description='ID of the owner')
})


@api.route('/')
class PlaceList(Resource):
    @jwt_required()  # task 3: Secure the Endpoints with JWT Authentication
    @api.expect(create_place_model)
    @api.response(201, 'Place successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new place"""
        current_user = get_jwt_identity()  # task 3: Identify currently logged-in user
        place_data = api.payload

        # Assign id of authenticated user to owner_id
        place_data['owner_id'] = current_user.get("id")  # task 3
        try:
            new_place = facade.create_place(place_data)

            response_data = {
                'id': new_place.id,
                'title': new_place.title,
                'description': new_place.description,
                'price': new_place.price,
                'latitude': new_place.latitude,
                'longitude': new_place.longitude,
                'owner': new_place.owner_id,
                'created_at': new_place.created_at.isoformat(),
                'updated_at': new_place.updated_at.isoformat()
            }

            return response_data, 201
        except Exception as e:
            api.abort(400, str(e))

    @api.response(200, 'List of places retrieved successfully')
    def get(self):
        """Retrieve a list of all places"""
        try:
            places = facade.get_all_places()

            # Manually serialize each place in the list
            places_data = []
            for place in places:

                place_data = {
                    'id': place.id,
                    'title': place.title,
                    'description': place.description,
                    'price': place.price,
                    'latitude': place.latitude,
                    'longitude': place.longitude,
                    'owner': place.owner_id,
                    'created_at': place.created_at.isoformat(),
                    'updated_at': place.updated_at.isoformat()
                }

                places_data.append(place_data)

            return places_data, 200
        except Exception as e:
            api.abort(400, str(e))


@api.route('/<place_id>')
class PlaceResource(Resource):
    @api.response(200, 'Place details retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get place details by ID"""
        try:
            place = facade.get_place(place_id)
            if not place:
                return {'error': 'Place not found'}, 404

            place_data = {
                'id': place.id,
                'title': place.title,
                'description': place.description,
                'price': place.price,
                'latitude': place.latitude,
                'longitude': place.longitude,
                'owner': place.owner_id,
                'created_at': place.created_at.isoformat(),
                'updated_at': place.updated_at.isoformat()
            }

            return place_data, 200
        except Exception as e:
            api.abort(400, str(e))

    @jwt_required()  # task 3: Secure the Endpoints with JWT Authentication
    @api.expect(create_place_model)
    @api.response(200, 'Place updated successfully')
    @api.response(404, 'Place not found')
    @api.response(400, 'Invalid input data')
    def put(self, place_id):
        """Update a place's information"""
        current_user = get_jwt_identity()  # task 3: Identify currently logged-in user
        place_data = api.payload
        try:
            updated_place = facade.update_place(place_id, place_data)
            if not updated_place:
                return {'error': 'Place not found'}, 404

            # task 3: If user is not owner, 403 error "Unauthorized action."
            if updated_place.user_id.id != current_user.get("id"):
                return {'error': 'Unauthorized action.'}, 403

            response_data = {
                'id': updated_place.id,
                'title': updated_place.title,
                'description': updated_place.description,
                'price': updated_place.price,
                'latitude': updated_place.latitude,
                'longitude': updated_place.longitude,
                'owner': updated_place.owner_id,
                'created_at': updated_place.created_at.isoformat(),
                'updated_at': updated_place.updated_at.isoformat()
            }

            return response_data, 200
        except Exception as e:
            return {'error': str(e)}, 400
