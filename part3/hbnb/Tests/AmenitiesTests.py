import unittest
from unittest.mock import patch
from part3.hbnb.app import create_app


class TestAmenityEndpoints(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        self.client.testing = True

    @patch('part2.hbnb.app.services.facade.create_amenity')
    def test_create_amenity_success(self, mock_create_amenity):
        # Mocking facade function to simulate amenity creation
        mock_create_amenity.return_value = type('Amenity', (), {
            'id': 'abcd1234',
            'name': 'Swimming Pool'
        })

        response = self.client.post('/api/v1/amenities/', json={
            'name': 'Swimming Pool'
        })

        self.assertEqual(response.status_code, 201)
        self.assertIn('id', response.json)
        self.assertEqual(response.json['name'], 'Swimming Pool')

    @patch('part2.hbnb.app.services.facade.create_amenity')
    def test_create_amenity_invalid_data(self, mock_create_amenity):
        # Mocking to raise an exception for invalid input data
        mock_create_amenity.side_effect = ValueError('Invalid input data')

        response = self.client.post('/api/v1/amenities/', json={
            'name': ''
        })

        self.assertEqual(response.status_code, 400)

    @patch('part2.hbnb.app.services.facade.get_all_amenities')
    def test_get_all_amenities(self, mock_get_all_amenities):
        # Mocking the retrieval of all amenities
        mock_get_all_amenities.return_value = [
            type('Amenity', (), {
                'id': 'abcd1234',
                'name': 'Swimming Pool'
            }),
            type('Amenity', (), {
                'id': 'efgh5678',
                'name': 'Gym'
            })
        ]

        response = self.client.get('/api/v1/amenities/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json), 2)
        self.assertEqual(response.json[0]['name'], 'Swimming Pool')
        self.assertEqual(response.json[1]['name'], 'Gym')

    @patch('part2.hbnb.app.services.facade.get_amenity')
    def test_get_amenity_success(self, mock_get_amenity):
        # Mocking successful retrieval of an amenity
        mock_get_amenity.return_value = type('Amenity', (), {
            'id': 'abcd1234',
            'name': 'Swimming Pool'
        })

        response = self.client.get('/api/v1/amenities/abcd1234')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['name'], 'Swimming Pool')

    @patch('part2.hbnb.app.services.facade.update_amenity')
    def test_update_amenity_success(self, mock_update_amenity):
        # Mocking successful amenity update
        mock_update_amenity.return_value = type('Amenity', (), {
            'id': 'abcd1234',
            'name': 'Updated Pool'
        })

        response = self.client.put('/api/v1/amenities/abcd1234', json={
            'name': 'Updated Pool'
        })

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['name'], 'Updated Pool')



if __name__ == '__main__':
    unittest.main()
