from datetime import datetime
from tests.setup import TestSetup
from consumeless import app, db
from models import User
import json
import jwt

class Login(TestSetup):

    def test_successful(self):
        tester = app.test_client(self)
        tester.post(
            'api/user/new',
             data=dict(username='new user', email='e@yahoo.com', password='test')
             )
        response = tester.post(
            'login',
             data=dict(username='new user', password='test')
             )
        response_message = json.loads(response.data)['message']
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response_message,
            'successfully logged in user: new user',
        )

    def test_invalid_password(self):
        tester = app.test_client(self)
        tester.post(
            'api/user/new',
             data=dict(username='new user', email='e@yahoo.com', password='test')
             )
        response = tester.post(
            'login',
             data=dict(username='new user', password='testing')
             )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            json.loads(response.data),
            {"error": "Invalid password"},
        )

    def test_insufficient_info(self):
        tester = app.test_client(self)
        tester.post(
            'api/user/new',
             data=dict(username='new user', email='e@yahoo.com', password='test')
             )
        response = tester.post(
            'login',
             data=dict(username='new user')
             )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            json.loads(response.data),
            {"error": "Insufficient information"},
        )

    def test_user_does_not_exist(self):
        tester = app.test_client(self)
        response = tester.post(
            'login',
            data=dict(username='user', password="pass")
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            json.loads(response.data),
            {"error": "User does not exist"},
        )

    def test_token_created(self):
        tester = app.test_client(self)
        register = tester.post(
            'api/user/new',
             data=dict(username='new user', email='e@yahoo.com', password='test')
             )
        login = tester.post(
            'login',
             data=dict(username='new user', password='test')
             )
        token = json.loads(login.data)['token']
        self.assertTrue(jwt.decode(token, app.config.get('SECRET_KEY')))

class Register(TestSetup):

    def test_token_created(self):
        tester = app.test_client(self)
        register = tester.post(
            'api/user/new',
             data=dict(username='new user', email='e@yahoo.com', password='test')
             )
        token = json.loads(register.data)['token']
        self.assertTrue(jwt.decode(token, app.config.get('SECRET_KEY')))

    def test_error_if_user_already_exists(self):
        tester = app.test_client(self)
        response = tester.post(
            'api/user/new',
             data=dict(username='new user', email='e@yahoo.com', password='test')
             )
        self.assertEqual(response.status_code, 200)
        self.assertRaises( Exception, tester.post(
            'api/user/new',
             data=dict(username='new user', email='e@yahoo.com', password='test')
             )
        )

    def test_user_added_to_database(self):
        tester = app.test_client(self)
        response = tester.post(
            'api/user/new',
             data=dict(username='new user', email='e@yahoo.com', password='test')
             )
        self.assertEqual(response.status_code, 200)
        self.assertIn( 'successfully added user: new user', json.loads(response.data)['message']
        )

class AddNewItem(TestSetup):

    def test_token_required(self):
        tester = app.test_client(self)
        register = tester.post(
            'api/user/new',
             data=dict(username='new user', email='e@yahoo.com', password='test')
             )
        response = tester.post(
            'api/item/new',
             data=dict(name='new item', description='test description', category='cat', email='e@yahoo.com', deposit=1.00, overdue_charge=1.00)
             )
        forbidden_error_code = 403
        self.assertEqual(response.status_code, forbidden_error_code)
