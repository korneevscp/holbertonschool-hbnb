#!/usr/bin/python3
from flask_restx import Namespace, Resource, fields
from part3.hbnb.app.services import facade
from flask_jwt_extended import jwt_required, get_jwt_identity

api = Namespace('placeamenities', description='Place Amenity Operations')

# Define the model with example data for better Swagger display
place_amenity_model = api.model('PlaceAmenity', {
    'place_id': fields.String(required=True, description='ID of the place', example='123'),
    'amenity_id': fields.String(required=True, description='ID of the amenity', example='456'),
})


@api.route('/')
class PlaceAmenities(Resource):
    def get(self):
        """Retrieve a list of amenities for places."""
        try:
            # Assuming facade.get_place_amenity() returns a list of place-amenity relationships
            place_amenities = facade.get_place_amenity()

            # Format the response data
            place_amenity_data = [
                {
                    'place_id': pa.place_id,
                    'amenity_id': pa.amenity_id
                } for pa in place_amenities
            ]
            return place_amenity_data, 200
        except Exception as e:
            return {'error': str(e)}, 400

    @jwt_required()
    @api.expect(place_amenity_model)  # This ensures the model is documented in Swagger
    def post(self):
        """Create a new place-amenity relationship."""
        current_user = get_jwt_identity()
        print("Current user identity:", current_user)

        # Get payload from the request
        place_amenity_data = api.payload
        if not place_amenity_data:
            return {'error': 'Invalid or missing JSON payload'}, 400

        # Validate the payload data
        if 'place_id' not in place_amenity_data or 'amenity_id' not in place_amenity_data:
            return {'error': 'place_id and amenity_id are required'}, 400

        # Validate place and amenity
        place = facade.get_place(place_amenity_data['place_id'])
        if not place:
            return {'error': 'Place Not Found'}, 404

        amenity = facade.get_amenity(place_amenity_data['amenity_id'])
        if not amenity:
            return {'error': 'Amenity Not Found'}, 404

        # Validate user
        user = facade.get_user(current_user['id'])
        if not user:
            return {'error': 'User Not Found'}, 404

        try:
            # Create a new place-amenity relationship
            new_place_amenity = facade.create_place_amenity(place_amenity_data)

            # Format the response
            created_place_amenity_data = {
                'place_id': new_place_amenity.place_id,
                'amenity_id': new_place_amenity.amenity_id
            }

            return created_place_amenity_data, 201
        except Exception as e:
            return {'error': str(e)}, 400
