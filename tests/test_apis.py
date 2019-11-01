from datetime import datetime
from tests.setup import TestSetup
from consumeless import app, db
from models import Item, User

class GetOneItem(TestSetup):

    def test_item_1_populated(self):
        newItem = Item(name = 'test',
                    description = "testing",
                    category = 'test',
                    email = 'test@gmail.com',
                    deposit = 1.00,
                    overdue_charge = 1.00,
                    created_at = datetime(2019, 11, 1))
        expected_output = b'{"category":"test","created_at":"01/11/2019","deposit":"1.0","description":"testing","email":"test@gmail.com","id":1,"name":"test","overdue_charge":"1.0"}\n'
        db.session.add(newItem)
        tester = app.test_client(self)
        response = tester.get('api/item/1', content_type='html/text')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, expected_output)

class GetItemException(TestSetup):

    def test_item_not_populated(self):
        tester = app.test_client(self)
        response = tester.get('api/item/4', content_type='html/text')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b'"\'NoneType\' object has no attribute \'serialize\'"\n')

class AddOneItem(TestSetup):

    def test_item_added_to_database(self):
        tester = app.test_client(self)
        response = tester.post(
            'api/item/new',
             data=dict(name='new item', description='test description', category='cat', email='e@yahoo.com', deposit=1.00, overdue_charge=1.00)
             )
        print(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b'successfully added item: new item')

class GetOneUSer(TestSetup):

    def test_user_1_populated(self):
        newUser = User(username = 'testuser',
                    email = 'testuser@gmail.com',
                    password_hash = 'test',
                    created_at = datetime(2019, 11, 1))
        expected_output = b'{"created_at":"01/11/2019","email":"testuser@gmail.com","id":1,"username":"testuser"}\n'
        db.session.add(newUser)
        tester = app.test_client(self)
        response = tester.get('api/user/1', content_type='html/text')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, expected_output)
