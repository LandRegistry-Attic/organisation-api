import unittest
import json

from organisation_api.main import app


class TestRoutes(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    def test_health(self):
        get_response = self.app.get('/health', headers={'Content-Type': 'application/json'})
        self.assertEqual(get_response.status_code, 200)

    def test_service_checks(self):
        service_list = {
            "status_code": 200,
            "service_from": "deed-api",
            "service_to": "organisation-api",
            "service_message": "Successfully connected"
        }
        get_response = self.app.get('/health/service-check', headers={'Content-Type': 'application/json'})
        self.assertEqual(get_response.status_code, 200)
        self.assertEqual(json.loads(get_response.data.decode('utf-8')), service_list)

    def test_get_organisation_name(self):
        # Setup organisation
        new_organisation = {"organisation_name": "integration test org",  "organisation_id": "9.9999"}
        post_response = self.app.post('/organisation-name', data=json.dumps(new_organisation),
                                      headers={'Content-Type': 'application/json', 'Accept': 'application/json'})
        self.assertEqual(post_response.status_code, 201)
        # Test the get endpoint
        get_response = self.app.get('/organisation-name/9.9999', headers={'Content-Type': 'application/json'})
        self.assertEqual(get_response.status_code, 200)
        self.assertEqual(json.loads(get_response.data.decode('utf-8')), {'organisation_name': 'integration test org'})
        # Teardown organisation
        delete_response = self.app.delete('/organisation-name/9.9999', headers={'Content-Type': 'application/json'})
        self.assertEqual(delete_response.status_code, 200)
        self.assertEqual(json.loads(delete_response.data.decode('utf-8')),
                         {'organisation_name': 'integration test org'})
