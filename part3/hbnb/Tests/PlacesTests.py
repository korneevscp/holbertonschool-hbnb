import unittest
from unittest.mock import patch
from part3.hbnb.app import create_app


class TestPlaceEndpoints(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        self.client.testing = True


    @patch('part2.hbnb.app.services.facade.get_place')
    def test_get_place_not_found(self, mock_get_place):
        # Mocking that the place is not found
        mock_get_place.return_value = None

        response = self.client.get('/api/v1/places/abcd1234')

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json['error'], 'Place not found')


    @patch('part2.hbnb.app.services.facade.update_place')
    def test_update_place_not_found(self, mock_update_place):
        # Mocking a place that is not found during update
        mock_update_place.return_value = None

        response = self.client.put('/api/v1/places/abcd1234', json={
            'title': 'Updated Apartment',
            'description': 'An updated cozy apartment',
            'price': 150.0,
            'latitude': 12.3456,
            'longitude': 65.4321,
            'owner_id': 'user1234',
            'amenities': ['amenity1234']
        })

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json['error'], 'Place not found')


if __name__ == '__main__':
    unittest.main()
