from flask_restx import Namespace, Resource, fields
from app.services import facade
from models.exceptions import ResourceNotFoundError, ValidationError

api = Namespace('reviews', description='Review operations')

# Models for documentation and validation
review_model = api.model('Review', {
    'text': fields.String(required=True, description="Review text"),
    'rating': fields.Integer(required=True, min=1, max=5, description="Rating (1-5)"),
    'user_id': fields.String(required=True, description="User ID"),
    'place_id': fields.String(required=True, description="Place ID")
})

review_response_model = api.inherit('ReviewResponse', review_model, {
    'id': fields.String(description="Unique review identifier"),
    'created_at': fields.DateTime(description="Creation date"),
    'updated_at': fields.DateTime(description="Last update date")
})

@api.route('/')
class ReviewList(Resource):
    @api.expect(review_model)
    @api.response(201, 'Review successfully created', review_response_model)
    @api.response(400, 'Invalid data')
    @api.response(404, 'User or place not found')
    def post(self):
        """Register a new review"""
        try:
            review = facade.create_review(api.payload)
            return review.to_dict(), 201
        except (ValidationError, ResourceNotFoundError) as e:
            api.abort(400 if isinstance(e, ValidationError) else 404, str(e))

    @api.response(200, 'List of reviews successfully retrieved', [review_response_model])
    def get(self):
        """Retrieve list of all reviews"""
        reviews = facade.get_all_reviews()
        return [review.to_dict() for review in reviews]

@api.route('/<review_id>')
@api.param('review_id', "Review identifier")
class ReviewResource(Resource):
    @api.response(200, 'Review details successfully retrieved', review_response_model)
    @api.response(404, 'Review not found')
    def get(self, review_id):
        """Get review details by ID"""
        try:
            review = facade.get_review(review_id)
            return review.to_dict()
        except ResourceNotFoundError as e:
            api.abort(404, str(e))

    @api.expect(review_model)
    @api.response(200, 'Review successfully updated', review_response_model)
    @api.response(404, 'Review not found')
    @api.response(400, 'Invalid data')
    def put(self, review_id):
        """Update review information"""
        try:
            review = facade.update_review(review_id, api.payload)
            return review.to_dict()
        except (ValidationError, ResourceNotFoundError) as e:
            api.abort(400 if isinstance(e, ValidationError) else 404, str(e))

    @api.response(200, 'Review successfully deleted')
    @api.response(404, 'Review not found')
    def delete(self, review_id):
        """Delete a review"""
        try:
            facade.delete_review(review_id)
            return {'message': 'Review successfully deleted'}
        except ResourceNotFoundError as e:
            api.abort(404, str(e))

@api.route('/places/<place_id>/reviews')
@api.param('place_id', "Place identifier")
class PlaceReviewList(Resource):
    @api.response(200, 'List of reviews for place successfully retrieved', [review_response_model])
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get all reviews for a specific place"""
        try:
            reviews = facade.get_reviews_by_place(place_id)
            return [review.to_dict() for review in reviews]
        except ResourceNotFoundError as e:
            api.abort(404, str(e))
