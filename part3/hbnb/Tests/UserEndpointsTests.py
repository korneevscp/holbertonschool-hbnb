import unittest
from unittest.mock import patch
from part3.hbnb.app import create_app


class TestUserEndpoints(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        self.client.testing = True

    @patch('part2.hbnb.app.services.facade.get_user_by_email')
    @patch('part2.hbnb.app.services.facade.create_user')
    def test_create_user(self, mock_create_user, mock_get_user_by_email):
        # Mocking facade functions to simulate database behavior
        mock_get_user_by_email.return_value = None
        mock_create_user.return_value = type('User', (), {
            'id': '1234',
            'first_name': 'Jane',
            'last_name': 'Doe',
            'email': 'jane.doe@example.com',
            'is_admin': False
        })

        response = self.client.post('/api/v1/users/', json={
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "jane.doe@example.com",
            "is_admin": False
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn('id', response.json)
        self.assertEqual(response.json['email'], 'jane.doe@example.com')

    @patch('part2.hbnb.app.services.facade.get_user_by_email')
    def test_create_user_duplicate_email(self, mock_get_user_by_email):
        # Mock email already exists
        mock_get_user_by_email.return_value = type('User', (), {'id': '1234'})

        response = self.client.post('/api/v1/users/', json={
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "jane.doe@example.com",
            "is_admin": False
        })
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['error'], 'Email already registered')

    @patch('part2.hbnb.app.services.facade.get_user')
    def test_get_user_success(self, mock_get_user):
        # Mock user retrieval
        mock_get_user.return_value = type('User', (), {
            'id': '1234',
            'first_name': 'Jane',
            'last_name': 'Doe',
            'email': 'jane.doe@example.com',
            'is_admin': False
        })

        response = self.client.get('/api/v1/users/1234')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['email'], 'jane.doe@example.com')

    @patch('part2.hbnb.app.services.facade.get_user')
    def test_get_user_not_found(self, mock_get_user):
        # Mock user not found
        mock_get_user.return_value = None

        response = self.client.get('/api/v1/users/1234')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json['error'], 'User not found')

    @patch('part2.hbnb.app.services.facade.get_all_users')
    def test_get_all_users(self, mock_get_all_users):
        # Mock getting all users
        mock_get_all_users.return_value = [
            type('User', (), {
                'id': '1234',
                'first_name': 'Jane',
                'last_name': 'Doe',
                'email': 'jane.doe@example.com',
                'is_admin': False
            }),
            type('User', (), {
                'id': '5678',
                'first_name': 'John',
                'last_name': 'Smith',
                'email': 'john.smith@example.com',
                'is_admin': True
            })
        ]

        response = self.client.get('/api/v1/users/user-list')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json), 2)
        self.assertEqual(response.json[0]['email'], 'jane.doe@example.com')
        self.assertEqual(response.json[1]['email'], 'john.smith@example.com')

    @patch('part2.hbnb.app.services.facade.update_user')
    def test_put_user_success(self, mock_update_user):
        # Mock user update
        mock_update_user.return_value = type('User', (), {
            'id': '1234',
            'first_name': 'Jane',
            'last_name': 'Smith',
            'email': 'jane.smith@example.com',
            'is_admin': False
        })

        response = self.client.put('/api/v1/users/update/1234', json={
            "first_name": "Jane",
            "last_name": "Smith",
            "email": "jane.smith@example.com",
            "is_admin": False
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['last_name'], 'Smith')

    @patch('part2.hbnb.app.services.facade.update_user')
    def test_put_user_not_found(self, mock_update_user):
        # Mock user not found for update
        mock_update_user.return_value = None

        response = self.client.put('/api/v1/users/update/1234', json={
            "first_name": "Jane",
            "last_name": "Smith",
            "email": "jane.smith@example.com",
            "is_admin": False
        })
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json['error'], 'User not found')


if __name__ == '__main__':
    unittest.main()
