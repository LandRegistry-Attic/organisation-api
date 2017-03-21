import unittest
import mock
from flask import Flask, request
import json
from jsonschema.exceptions import ValidationError
from organisation_api.views.organisation_name import get_organisation_name, post_organisation_name, \
    delete_organisation_name
from organisation_api.models import Organisation


class DatabaseStub(list):  # Observe - inherits from a list, so mimics parts of a database result.

    def __init__(self, result_count):
        self.result_count = result_count

    def count(self):
        return self.result_count


def stub_get_json():
    return {'a': 'b'}


class TestOrganisationName(unittest.TestCase):

    @mock.patch('organisation_api.views.organisation_name.get_organisation', autospec=False)
    def test_get_organisation_name_404(self, mock_get_organisation):
        mock_get_organisation.return_value = DatabaseStub(0)
        app = Flask(__name__)
        with app.app_context():
            with app.test_request_context():
                resp = get_organisation_name('dummy')
                self.assertEqual(str(resp.mimetype), "application/json")
                self.assertEqual(resp.status, '404 NOT FOUND')
                self.assertEqual(json.loads(resp.data.decode("utf-8")), {"organisation_name": "not found"})

    @mock.patch('organisation_api.views.organisation_name.get_organisation', autospec=False)
    def test_get_organisation_name_200(self, mock_get_organisation):
        stub_database = DatabaseStub(1)
        organisation = Organisation()
        organisation.organisation_name = 'A Bank'
        stub_database.append(organisation)
        mock_get_organisation.return_value = stub_database
        app = Flask(__name__)
        with app.app_context():
            with app.test_request_context():
                resp = get_organisation_name('dummy')
                self.assertEqual(str(resp.mimetype), "application/json")
                self.assertEqual(resp.status, '200 OK')
                self.assertEqual(json.loads(resp.data.decode('utf-8')), {'organisation_name': 'A Bank'})

    @mock.patch('organisation_api.views.organisation_name.Organisation', autospec=False)
    def test_post_organisation_name_201(self, mock_Organisation):
        app = Flask(__name__)
        with app.app_context():
            with app.test_request_context():

                def stub_get_json():
                    return {"organisation_name": "Bananas",  "organisation_id": "10.1.1"}

                request.get_json = stub_get_json
                resp = post_organisation_name()
                self.assertEqual(str(resp.mimetype), "application/json")
                self.assertEqual(resp.status, '201 CREATED')
                self.assertEqual(json.loads(resp.data.decode('utf-8')), {'path': '/organisation-name/10.1.1'})

    def test_post_organisation_name_fails_schema(self):
        app = Flask(__name__)
        with app.app_context():
            with app.test_request_context():

                def stub_get_json():
                    return {"organisation_n@@@@@@@@@me": "Bananas",  "organisation_id": "10.1.1"}

                request.get_json = stub_get_json
                self.assertRaises(ValidationError, post_organisation_name)

    @mock.patch('organisation_api.views.organisation_name.Organisation', autospec=False)
    @mock.patch('organisation_api.views.organisation_name.get_organisation', autospec=False)
    def test_delete_organisation_name_200(self, mock_get_organisation, mock_organisation):
        stub_database = DatabaseStub(1)
        mock_organisation.organisation_name = 'A Bank'
        stub_database.append(mock_organisation)
        mock_get_organisation.return_value = stub_database
        app = Flask(__name__)
        with app.app_context():
            with app.test_request_context():
                resp = delete_organisation_name('dummy')
                self.assertEqual(str(resp.mimetype), "application/json")
                self.assertEqual(resp.status, '200 OK')
                self.assertEqual(json.loads(resp.data.decode('utf-8')), {'organisation_name': 'A Bank'})

    @mock.patch('organisation_api.views.organisation_name.Organisation', autospec=False)
    @mock.patch('organisation_api.views.organisation_name.get_organisation', autospec=False)
    def test_delete_organisation_name_404(self, mock_get_organisation, mock_organisation):
        stub_database = DatabaseStub(0)
        mock_organisation.organisation_name = 'A Bank'
        stub_database.append(mock_organisation)
        mock_get_organisation.return_value = stub_database
        #  This test uses an alternative method of creating the test context using the actual app from the
        # imported flask application. Consider testing from routes in the future using examples in gadgets.
        from organisation_api.main import app

        with app.app_context() as ac:
            ac.g.trace_id = None
            with app.test_request_context():
                resp = delete_organisation_name('dummy')
                self.assertEqual(str(resp.mimetype), "application/json")
                self.assertEqual(resp.status, '404 NOT FOUND')
                self.assertEqual(json.loads(resp.data.decode('utf-8')), {'organisation_name': 'not found'})
