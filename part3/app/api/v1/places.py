from flask_restx import Namespace, Resource, fields
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.facade import HBnBFacade

facade = HBnBFacade()

def validate_place_data(data, update=False):
    """Validate the place data. If update=True, owner_id is not required."""
    required_fields = ['title', 'price', 'latitude', 'longitude', 'amenities']
    if not update:
        required_fields.append('owner_id')  # Owner ID est obligatoire pour la création

    for field in required_fields:
        if field not in data or data[field] is None:
            return False
    return True

api = Namespace('places', description='Place operations')

place_model = api.model('Place', {
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude of the place'),
    'longitude': fields.Float(required=True, description='Longitude of the place'),
    'amenities': fields.List(fields.String, required=True, description="List of amenities ID's")
})

@api.route('/')
class PlaceList(Resource):
    @jwt_required()
    @api.expect(place_model)
    @api.response(201, 'Place successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Créer un nouveau lieu 🔐 (Requiert authentification)"""
        current_user_id = get_jwt_identity()  # Récupérer l'ID de l'utilisateur connecté
        place_data = api.payload

        if not place_data or not validate_place_data(place_data):
            return {'error': 'Invalid input data'}, 400

        # Forcer le owner_id à être celui de l'utilisateur connecté
        place_data['owner_id'] = current_user_id

        new_place = facade.create_place(place_data)
        return {'message': 'Place successfully created', 'id': new_place.id}, 201

    @api.response(200, 'List of places retrieved successfully')
    def get(self):
        """🔓 Public: Récupérer une liste de tous les lieux disponibles"""
        places = facade.get_all_places()
        return [{'id': place.id, 'latitude': place.latitude, 'longitude': place.longitude, 
                 'owner_id': place.owner_id, 'amenities': place.amenities} for place in places], 200

@api.route('/<place_id>')
class PlaceResource(Resource):
    @api.response(200, 'Place details retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """🔓 Public: Récupérer les détails d'un lieu spécifique"""
        place = facade.get_place_by_id(place_id)
        if not place:
            return {'error': 'Place not found'}, 404
        return place, 200

    @jwt_required()
    @api.expect(place_model)
    @api.response(200, 'Place updated successfully')
    @api.response(403, 'Unauthorized action')
    @api.response(404, 'Place not found')
    @api.response(400, 'Invalid input data')
    def put(self, place_id):
        """Modifier un lieu - 🔐 Seul le propriétaire peut le faire"""
        current_user_id = get_jwt_identity()
        data = request.json
        place = facade.get_place_by_id(place_id)

        if not place:
            return {'error': 'Place not found'}, 404
        if not validate_place_data(data, update=True):
            return {'error': 'Invalid input data'}, 400
        if place.owner_id != current_user_id:
            return {'error': 'Unauthorized action'}, 403

        # Empêcher la modification de owner_id
        if 'owner_id' in data and data['owner_id'] != place.owner_id:
            return {'error': 'Forbidden: owner_id cannot be changed'}, 403

        facade.update_place(place_id, data)
        return {'message': 'Place updated successfully'}, 200

    @jwt_required()
    @api.response(200, 'Place deleted successfully')
    @api.response(403, 'Unauthorized action')
    @api.response(404, 'Place not found')
    def delete(self, place_id):
        """Supprimer un lieu - 🔐 Seul le propriétaire peut le faire"""
        current_user_id = get_jwt_identity()
        place = facade.get_place_by_id(place_id)

        if not place:
            return {'error': 'Place not found'}, 404
        if place.owner_id != current_user_id:
            return {'error': 'Unauthorized action'}, 403

        facade.delete_place(place_id)
        return {'message': 'Place deleted successfully'}, 200