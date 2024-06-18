import unittest
from unittest.mock import patch
from flask import jsonify
from app import app
from app.auth_middleware import admin_access_required, manager_access_required
from app.models import User


class MiddlewareTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    @patch('app.auth_middleware.get_jwt_identity')
    @patch('app.auth_middleware.User.get_by_username')
    def test_admin_access_required(self, mock_get_by_username, mock_get_jwt_identity):
        mock_get_jwt_identity.return_value = 'admin_user'
        mock_get_by_username.return_value = User(username='admin_user', role='Admin')

        @admin_access_required
        def dummy_route():
            return jsonify(message="Admin access granted")

        with app.app_context():
            with self.app as client:
                with client.session_transaction() as sess:
                    response = dummy_route()
                    self.assertEqual(response.status_code, 200)
                    self.assertIn(b"Admin access granted", response.data)

    @patch('app.auth_middleware.get_jwt_identity')
    @patch('app.auth_middleware.User.get_by_username')
    def test_manager_access_required(self, mock_get_by_username, mock_get_jwt_identity):
        mock_get_jwt_identity.return_value = 'manager_user'
        mock_get_by_username.return_value = User(username='manager_user', role='Manager')

        @manager_access_required
        def dummy_route():
            return jsonify(message="Manager access granted")

        with app.app_context():
            with self.app as client:
                with client.session_transaction() as sess:
                    response = dummy_route()
                    self.assertEqual(response.status_code, 200)
                    self.assertIn(b"Manager access granted", response.data)


if __name__ == '__main__':
    unittest.main()
