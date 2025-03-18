import unittest
from unittest.mock import patch
from part3.hbnb.app import create_app


class TestReviewEndpoints(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        self.client.testing = True

    @patch('part2.hbnb.app.services.facade.get_review')
    def test_get_review_not_found(self, mock_get_review):
        # Mocking that the review is not found
        mock_get_review.return_value = None

        response = self.client.get('/api/v1/reviews/review1234')

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json['error'], 'Review does not exist')


    @patch('part2.hbnb.app.services.facade.update_review')
    def test_update_review_not_found(self, mock_update_review):
        # Mocking a review that is not found during update
        mock_update_review.return_value = None

        response = self.client.put('/api/v1/reviews/review1234', json={
            'text': 'Updated review!',
            'rating': 4,
            'user_id': 'user1234',
            'place_id': 'place1234'
        })

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json['error'], 'Review does not exist')

    @patch('part2.hbnb.app.services.facade.delete_review')
    def test_delete_review_success(self, mock_delete_review):
        # Mocking successful deletion of a review
        mock_delete_review.return_value = True

        response = self.client.delete('/api/v1/reviews/review1234')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['message'], 'Review deleted successfully')

    @patch('part2.hbnb.app.services.facade.delete_review')
    def test_delete_review_not_found(self, mock_delete_review):
        # Mocking a review that is not found during deletion
        mock_delete_review.return_value = None

        response = self.client.delete('/api/v1/reviews/review1234')

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json['error'], 'Review does not exist')


if __name__ == '__main__':
    unittest.main()
