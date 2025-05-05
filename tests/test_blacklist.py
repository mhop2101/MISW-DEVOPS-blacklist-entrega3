import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from unittest.mock import patch, MagicMock
from application import application
from flask_jwt_extended import create_access_token


class TestRoutes(unittest.TestCase):
    def setUp(self):
        self.app = application.test_client()
        self.app_ctx = application.app_context()
        self.app_ctx.push()

        # Generar un JWT válido para las pruebas protegidas
        with application.app_context():
            self.token = create_access_token(identity='test-user', expires_delta=False)
        self.auth_header = {'Authorization': f'Bearer {self.token}'}

        # Patch a la consulta de SQLAlchemy
        self.patcher_query = patch('models.blacklist.Blacklist.query')
        self.mock_query = self.patcher_query.start()

        # Patch al db.session
        self.patcher_session = patch('extensions.db.session')
        self.mock_session = self.patcher_session.start()

    def tearDown(self):
        self.patcher_query.stop()
        self.patcher_session.stop()
        self.app_ctx.pop()

    def test_health(self):
        response = self.app.get('/health')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.get_json(), {'status': 'ok'})

    def test_login(self):
        response = self.app.get('/login')
        self.assertEqual(response.status_code, 200)
        self.assertIn('token', response.get_json())

    def test_add_to_blacklist_missing_field(self):
        data = {
            'email': '',
            'app_uuid': '123e4567-e89b-12d3-a456-426614174000',
            'blocked_reason': 'Test'
        }
        response = self.app.post('/blacklists', json=data, headers=self.auth_header)
        self.assertEqual(response.status_code, 400)
        self.assertIn('message', response.get_json())

    def test_add_to_blacklist_invalid_email(self):
        data = {
            'email': 'invalido',
            'app_uuid': '123e4567-e89b-12d3-a456-426614174000',
            'blocked_reason': 'Test'
        }
        response = self.app.post('/blacklists', json=data, headers=self.auth_header)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json()['message'], 'Formato de email inválido')

    def test_add_to_blacklist_invalid_uuid(self):
        data = {
            'email': 'test@example.com',
            'app_uuid': 'uuid-invalido',
            'blocked_reason': 'Test'
        }
        response = self.app.post('/blacklists', json=data, headers=self.auth_header)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json()['message'], 'Formato de UUID inválido')

    def test_add_to_blacklist_existing_email(self):
        # Simula que el email ya está en la lista negra
        mock_record = MagicMock()
        self.mock_query.filter_by.return_value.first.return_value = mock_record

        data = {
            'email': 'test@example.com',
            'app_uuid': '123e4567-e89b-12d3-a456-426614174000',
            'blocked_reason': 'Test'
        }
        response = self.app.post('/blacklists', json=data, headers=self.auth_header)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json()['message'], 'Email ya está en la lista negra')

    def test_add_to_blacklist_success(self):
        # Simula que no hay email existente
        self.mock_query.filter_by.return_value.first.return_value = None

        data = {
            'email': 'nuevo@example.com',
            'app_uuid': '123e4567-e89b-12d3-a456-426614174000',
            'blocked_reason': 'Motivo válido'
        }
        response = self.app.post('/blacklists', json=data, headers=self.auth_header)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.get_json()['message'], 'Email agregado a la lista negra')

    def test_check_blacklist_found(self):
        mock_record = MagicMock()
        mock_record.blocked_reason = 'Razón'
        self.mock_query.filter_by.return_value.first.return_value = mock_record

        response = self.app.get('/blacklists/test@example.com', headers=self.auth_header)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {
            'blacklisted': True,
            'blocked_reason': 'Razón'
        })

    def test_check_blacklist_not_found(self):
        self.mock_query.filter_by.return_value.first.return_value = None

        response = self.app.get('/blacklists/test@example.com', headers=self.auth_header)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {
            'blacklisted': False
        })


if __name__ == '__main__':
    unittest.main()