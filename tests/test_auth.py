from datetime import datetime
from tests.setup import TestSetup
from consumeless import app, db
from models import User

class Login(TestSetup):

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
        self.assertEqual(response.data, b'Well Done')
