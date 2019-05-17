from app import app, db
from flask_testing import TestCase
import json


class BaseTestCase(TestCase):
    def create_app(self):
        """
        Create an instance of the app with the testing configuration
        :return:
        """
        app.config.from_object('app.config.TestingConfig')
        return app

    def setUp(self):
        """
        Create the database
        :return:
        """
        db.create_all()
        db.session.commit()

    def tearDown(self):
        """
        Drop the database tables and also remove the session
        :return:
        """
        db.session.remove()
        db.drop_all()

    def register_user(self, email, password):
        """
        Helper method for registering a user with dummy data
        :return:
        """
        return self.client.post(
            'v1/auth/register',
            content_type='application/json',
            data=json.dumps(dict(email=email, password=password)))

    def get_user_token(self):
        """
        Get a user token
        :return:
        """
        auth_res = self.register_user('example@gmail.com', '123456')
        return json.loads(auth_res.data.decode())['auth_token']

    def create_store(self, token):
        """
        Helper function to create a store
        :return:
        """
        response = self.client.post(
            'v1/storelists/',
            data=json.dumps(dict(name='Travel')),
            headers=dict(Authorization='Bearer ' + token),
            content_type='application/json'
        )
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 201)
        self.assertTrue(data['status'], 'success')
        self.assertTrue(data['name'], 'Travel')
        self.assertIsInstance(data['id'], int, msg='Value should be a string')

    def create_stores(self, token):
        """
        Helper function to create a store
        :return:
        """
        stores = [
            {'name': 'Travel'},
            {'name': 'Tral'},
            {'name': 'Trvel'},
            {'name': 'Tavel'},
            {'name': 'Travl'},
            {'name': 'Trave'},
        ]
        for store in stores:
            response = self.client.post(
                'v1/storelists/',
                data=json.dumps(dict(name=store['name'])),
                headers=dict(Authorization='Bearer ' + token),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            self.assertTrue(data['status'], 'success')
            self.assertTrue(data['name'], store['name'])
            self.assertIsInstance(data['id'], int, msg='Value should be a string')
