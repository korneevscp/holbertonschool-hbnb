from flask_restx import Namespace, Resource, fields
from flask import request
from app.services import facade

api = Namespace('amenities', description='Amenity operations')

# Define the amenity model for input validation and documentation
amenity_model = api.model('Amenity', {
    'name': fields.String(required=True, description='Name of the amenity')
})

amenity_response_model = api.model('AmenityResponse', {
    'id': fields.String(description='Unique identifier of the amenity'),
    'name': fields.String(description='Name of the amenity')
})

@api.route('/')
class AmenityList(Resource):
    @api.expect(amenity_model)
    @api.response(201, 'Amenity successfully created', amenity_response_model)
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new amenity"""
        try:
            amenity = facade.create_amenity(request.json)
            return {
                'id': amenity.id,
                'name': amenity.name
            }, 201
        except ValueError as e:
            api.abort(400, str(e))

    @api.response(200, 'List of amenities retrieved successfully', [amenity_response_model])
    def get(self):
        """Retrieve a list of all amenities"""
        amenities = facade.get_all_amenities()
        return [{'id': amenity.id, 'name': amenity.name} for amenity in amenities], 200

@api.route('/<amenity_id>')
class AmenityResource(Resource):
    @api.response(200, 'Amenity details retrieved successfully', amenity_response_model)
    @api.response(404, 'Amenity not found')
    def get(self, amenity_id):
        """Get amenity details by ID"""
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            api.abort(404, "Amenity not found")
        
        return {
            'id': amenity.id,
            'name': amenity.name
        }, 200

    @api.expect(amenity_model)
    @api.response(200, 'Amenity updated successfully')
    @api.response(404, 'Amenity not found')
    @api.response(400, 'Invalid input data')
    def put(self, amenity_id):
        """Update an amenity's information"""
        try:
            amenity = facade.update_amenity(amenity_id, request.json)
            if not amenity:
                api.abort(404, "Amenity not found")
            
            return {
                'message': 'Amenity updated successfully'
            }, 200
        except ValueError as e:
            api.abort(400, str(e))
