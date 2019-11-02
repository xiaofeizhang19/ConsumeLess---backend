from datetime import datetime
from tests.setup import TestSetup
from consumeless import app, db
from models import User
import json

class SuccessfulLogin(TestSetup):

    def test_login(self):
        tester = app.test_client(self)
        tester.post(
            'api/user/new',
             data=dict(username='new user', email='e@yahoo.com', password='test')
             )
        response = tester.post(
            'login',
             data=dict(username='new user', password='test')
             )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            json.loads(response.data),
            {'message': 'Well done'},
        )

class UnsuccessfulLogin(TestSetup):

    def test_login(self):
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

class MoreUnsuccessfulLogin(TestSetup):

    def test_login(self):
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

class UnsuccessfulLoginWhenUserDoesNotExist(TestSetup):

    def test_login(self):
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
