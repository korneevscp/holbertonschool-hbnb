#!/usr/bin/python3
from flask_restx import Namespace, Resource, fields
from part3.hbnb.app.services import facade
from flask_jwt_extended import jwt_required, get_jwt_identity


api = Namespace('reviews', description='Review operations')

# Define the review model for input validation and documentation
review_model = api.model('Review', {
    'text': fields.String(required=True, description='Text of the review'),
    'rating': fields.Integer(required=True, description='Rating of the place (1-5)'),
    'user_id': fields.String(required=True, description='ID of the user'),
    'place_id': fields.String(required=True, description='ID of the place')
})


@api.route('/')
class ReviewList(Resource):
    @jwt_required()  # task 3: Secure Endpoints with JWT Authentication
    @api.expect(review_model)
    @api.response(201, 'Review successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new review"""
        current_user = get_jwt_identity()  # task 3: Identify currently logged-in user
        review_data = api.payload

        # Check if user is owner of place
        place = facade.get_place(review_data['place_id'])
        if not place:
            return 'Error Not Found', 404

        # Owner is not allowed to review their own place
        if place.owner_id == current_user.get("id"):
            return 'You cannot review your own place.', 400

        # Check if user already left a review
        review = facade.get_reviews_by_place(review_data['place_id'])
        for review in review:
            if review.user_id == current_user.get("id"):
                return 'You have already reviewed this place..', 400

        try:
            review_data['user_id'] = current_user.get("id")
            new_review = facade.create_review(review_data)

            # Serialize the review
            review_data = {
                'id': new_review.id,
                'text': new_review.text,
                'rating': new_review.rating,
                'place_id': new_review.place_id,
                'user_id': new_review.user_id,
                'created_at': new_review.created_at.isoformat(),
                'updated_at': new_review.updated_at.isoformat()
            }

            return review_data, 201
        except Exception as e:
            return {'error': str(e)}, 400

    @api.response(200, 'List of reviews retrieved successfully')
    def get(self):
        """Retrieve a list of all reviews"""
        try:
            reviews = facade.get_all_reviews()

            # Manually serialize each review
            reviews_data = [
                {
                    'id': review.id,
                    'text': review.text,
                    'rating': review.rating,
                    'place_id': review.place_id,
                    'user_id': review.user_id,
                    'created_at': review.created_at.isoformat(),
                    'updated_at': review.updated_at.isoformat()
                } for review in reviews
            ]

            return reviews_data, 200
        except Exception as e:
            return {'error': str(e)}, 400


@api.route('/<review_id>')
class ReviewResource(Resource):
    @jwt_required()
    @api.response(200, 'Review details retrieved successfully')
    @api.response(404, 'Review not found')
    def get(self, review_id):
        """Get review details by ID"""
        review = facade.get_review(review_id)
        if review:
            # Serialize the review
            review_data = {
                'id': review.id,
                'text': review.text,
                'rating': review.rating,
                'place_id': review.place_id,
                'user_id': review.user_id,
                'created_at': review.created_at.isoformat(),
                'updated_at': review.updated_at.isoformat()
            }
            return review_data, 200
        else:
            return {'error': 'Review does not exist'}, 404

    @jwt_required()  # task 3: Secure Endpoints with JWT Authentication
    @api.expect(review_model)
    @api.response(200, 'Review updated successfully')
    @api.response(404, 'Review not found')
    @api.response(400, 'Invalid input data')
    def put(self, review_id):
        """Update a review's information"""
        current_user = get_jwt_identity()  # task 3: Identify currently logged-in user
        review_data = api.payload

        review = facade.get_review(review_id)  # task 3: Check user_id matches  authenticated user.

        if review.user_id != current_user.get("id"):
            return {'error': 'Unauthorized action.'}, 403

        try:
            updated_review = facade.update_review(review_id, review_data)
            if updated_review:
                # Serialize the updated review
                review_data = {
                    'id': updated_review.id,
                    'text': updated_review.text,
                    'rating': updated_review.rating,
                    'place_id': updated_review.place_id,
                    'user_id': updated_review.user_id,
                    'created_at': updated_review.created_at.isoformat(),
                    'updated_at': updated_review.updated_at.isoformat()
                }
                return review_data, 200
            else:
                return {'error': 'Review does not exist'}, 404
        except Exception as e:
            return {'error': str(e)}, 400

    @jwt_required()
    @api.response(200, 'Review deleted successfully')
    @api.response(404, 'Review not found')
    def delete(self, review_id):
        """Delete a review"""
        current_user = get_jwt_identity()  # task 3: Ensure the user is authenticated
        review = facade.get_review(review_id)  # task 3: Check user_id matches  authenticated user.

        if review.user_id != current_user.get("id"):
            return {'error': 'Unauthorized action.'}, 403

        try:
            delete_review = facade.delete_review(review_id)
            if delete_review:
                return {'message': 'Review deleted successfully'}, 200
            else:
                return {'error': 'Review does not exist'}, 404
        except Exception as e:
            return {'error': str(e)}, 400


@api.route('/places/<place_id>/reviews')
class PlaceReviewList(Resource):
    @api.response(200, 'List of reviews for the place retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get all reviews for a specific place"""
        try:
            reviews = facade.get_reviews_by_place(place_id)
            if reviews:
                # Manually serialize each review
                reviews_data = [
                    {
                        'id': review.id,
                        'text': review.text,
                        'rating': review.rating,
                        'place_id': review.place_id,
                        'user_id': review.user_id,
                        'created_at': review.created_at.isoformat(),
                        'updated_at': review.updated_at.isoformat()
                    } for review in reviews
                ]

                return reviews_data, 200
            else:
                return {'error': 'Place does not exist or has no reviews'}, 404
        except Exception as e:
            return {'error': str(e)}, 400
