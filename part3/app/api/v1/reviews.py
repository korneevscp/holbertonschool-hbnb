from flask_restx import Namespace, Resource, fields
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.facade import HBnBFacade

api = Namespace('reviews', description='Review operations')
facade = HBnBFacade()

# Modèle de validation des avis
review_model = api.model('Review', {
    'text': fields.String(required=True, description='Text of the review'),
    'rating': fields.Integer(required=True, description='Rating (1-5)'),
    'place_id': fields.String(required=True, description='ID of the place')
})

@api.route('/')
class ReviewList(Resource):
    @jwt_required()
    @api.expect(review_model)
    @api.response(201, 'Review successfully created')
    @api.response(400, 'Invalid input data')
    @api.response(403, 'Forbidden: You cannot review your own place')
    @api.response(409, 'Conflict: You have already reviewed this place')
    def post(self):
        """Créer un avis - 🔐 Seul un utilisateur authentifié peut laisser un avis"""
        current_user_id = get_jwt_identity()
        review_data = api.payload

        if not review_data:
            return {'error': 'Invalid input data'}, 400
        
        place_id = review_data['place_id']

        # Vérifier si le lieu existe
        place = facade.get_place_by_id(place_id)
        if not place:
            return {'error': 'Place not found'}, 404

        # Vérifier si l'utilisateur tente de noter son propre lieu
        if place.owner_id == current_user_id:
            return {'error': 'Forbidden: You cannot review your own place'}, 403

        # Vérifier si l'utilisateur a déjà laissé un avis pour ce lieu
        existing_review = facade.get_review_by_user_and_place(current_user_id, place_id)
        if existing_review:
            return {'error': 'Conflict: You have already reviewed this place'}, 409

        # Créer l'avis
        review_data['user_id'] = current_user_id
        new_review = facade.create_review(review_data)
        return {'message': 'Review successfully created', 'id': new_review.id}, 201

    @api.response(200, 'List of reviews retrieved successfully')
    def get(self):
        """🔓 Public: Récupérer tous les avis"""
        reviews = facade.get_all_reviews()
        return [{'id': review.id, 'text': review.text, 'rating': review.rating, 'user_id': review.user_id, 'place_id': review.place_id} for review in reviews], 200


@api.route('/<review_id>')
class ReviewResource(Resource):
    @api.response(200, 'Review details retrieved successfully')
    @api.response(404, 'Review not found')
    def get(self, review_id):
        """🔓 Public: Récupérer un avis spécifique"""
        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404
        return {'id': review.id, 'text': review.text, 'rating': review.rating, 'user_id': review.user_id, 'place_id': review.place_id}, 200

    @jwt_required()
    @api.expect(review_model)
    @api.response(200, 'Review updated successfully')
    @api.response(403, 'Forbidden: You can only edit your own reviews')
    @api.response(404, 'Review not found')
    def put(self, review_id):
        """Modifier un avis - 🔐 Seul l'auteur de l'avis peut le modifier"""
        current_user_id = get_jwt_identity()
        review_data = api.payload

        if not review_data:
            return {'error': 'Invalid input data'}, 400

        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404

        # Vérifier si l'utilisateur est bien l'auteur de l'avis
        if review.user_id != current_user_id:
            return {'error': 'Forbidden: You can only edit your own reviews'}, 403

        facade.update_review(review_id, review_data)
        return {'message': 'Review updated successfully'}, 200

    @jwt_required()
    @api.response(200, 'Review deleted successfully')
    @api.response(403, 'Forbidden: You can only delete your own reviews')
    @api.response(404, 'Review not found')
    def delete(self, review_id):
        """Supprimer un avis - 🔐 Seul l'auteur de l'avis peut le supprimer"""
        current_user_id = get_jwt_identity()
        review = facade.get_review(review_id)

        if not review:
            return {'error': 'Review not found'}, 404

        if review.user_id != current_user_id:
            return {'error': 'Forbidden: You can only delete your own reviews'}, 403

        facade.delete_review(review_id)
        return {'message': 'Review deleted successfully'}, 200


@api.route('/places/<place_id>/reviews')
class PlaceReviewList(Resource):
    @api.response(200, 'List of reviews for the place retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """🔓 Public: Récupérer tous les avis d'un lieu"""
        reviews = facade.get_reviews_by_place(place_id)
        if not reviews:
            return {'error': 'No reviews found for this place'}, 404
        return [{'id': review.id, 'text': review.text, 'rating': review.rating, 'user_id': review.user_id, 'place_id': review.place_id} for review in reviews], 200
