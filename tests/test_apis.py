from datetime import datetime, date, timedelta
from tests.setup import TestSetup
from consumeless import app, db
from models import Item, User
import json

class ItemAPIs(TestSetup):

    def test_1_populated(self):
        newUser = User(username = 'testuser',
                    email = 'testuser@gmail.com',
                    password_hash = 'test',
                    created_at = datetime(2019, 11, 1),
                    postcode = 'e49qr',
                    latitude = 51.7655451,
                    longitude = -1.257095)
        db.session.add(newUser)
        newItem = Item(name = 'test',
                    description = "testing",
                    category = 'test',
                    owner_id = 1,
                    deposit = 1.00,
                    overdue_charge = 1.00,
                    created_at = datetime(2019, 11, 1))
        expected_output = b'{"category":"test","created_at":"01/11/2019","deposit":"1.0","description":"testing","id":1,"latitude":51.7655451,"longitude":-1.257095,"name":"test","overdue_charge":"1.0","owner_id":1}\n'
        db.session.add(newItem)
        db.session.commit()
        tester = app.test_client(self)
        response = tester.get('api/item/1', content_type='html/text')
        print(response.data)
        # print(blah)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, expected_output)

    def test_item_not_found(self):
        tester = app.test_client(self)
        response = tester.get('api/item/4', content_type='html/text')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            json.loads(response.data),
            {"error": "Item not found"},
        )

    def test_item_added_to_database(self):
        tester = app.test_client(self)
        login = tester.post(
            'api/user/new',
             data=dict(username='new user', email='e@yahoo.com', password='test')
             )
        token = json.loads(login.data)['token']
        response = tester.post(
            f'api/item/new?token={token}',
             data=dict(name='new item', description='test description', category='cat', deposit=1.00, overdue_charge=1.00)
             )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            json.loads(response.data),
            {'message': 'successfully added item: new item'},
        )

    def test_fail_if_token_expired(self):
        tester = app.test_client(self)
        token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE1NzI3MTgzMDEsImlhdCI6MTU3MjcxODI3MSwic3ViIjoxOH0.AIBoO1qbh0KHDKnAs56NP2BVH8NoO2jFgNmN7RUKxYw'
        self.assertRaises(
            Exception, tester.post(
                f'api/item/new?token={token}',
                 data=dict(name='new item', description='test description', category='cat', email='e@yahoo.com', deposit=1.00, overdue_charge=1.00)
                 ))

    def test_missing_params_raises_error(self):
        tester = app.test_client(self)
        self.assertRaises(Exception, tester.post(
            'api/item/new',
             data=dict(name='new item', category='cat', email='e@yahoo.com', deposit=1.00, overdue_charge=1.00)
             ))

    def test_my_items_displayed(self):
        tester = app.test_client()
        # register a user and get token
        register = tester.post(
            'api/user/new',
             data=dict(username='new user', email='e@yahoo.com', password='test')
             )
        token = json.loads(register.data)['token']
        # add an item to db
        tester.post(
            f'api/item/new?token={token}',
             data=dict(name='new item', description='test description', category='cat', deposit=1.00, overdue_charge=1.00)
             )
        # access our items
        response = tester.get(
            f'api/items?token={token}',
            content_type='html/text'
            )
        self.assertIn(b'new item', response.data)
        # register a new user and get new token
        register = tester.post(
            'api/user/new',
             data=dict(username='second user', email='e2@yahoo.com', password='test')
             )
        token = json.loads(register.data)['token']
        # access our items, as different user (expect none)
        response = tester.get(
            f'api/items?token={token}',
            content_type='html/text'
            )
        self.assertNotIn(b'new item', response.data)

class UserAPIs(TestSetup):

    def test_user_1_populated(self):
        newUser = User(username = 'testuser',
                    email = 'testuser@gmail.com',
                    password_hash = 'test',
                    created_at = datetime(2019, 11, 1),
                    postcode = 'e49qr',
                    latitude = 51.7655451,
                    longitude = -1.257095)
        expected_output = b'{"created_at":"01/11/2019","email":"testuser@gmail.com","id":1,"latitude":51.7655451,"longitude":-1.257095,"postcode":"e49qr","username":"testuser"}\n'
        db.session.add(newUser)
        db.session.commit()
        tester = app.test_client(self)
        response = tester.get('api/user/1', content_type='html/text')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, expected_output)

    def test_missing_email_raises_error(self):
        tester = app.test_client(self)
        self.assertRaises(Exception, tester.post(
            'api/user/new',
             data=dict(username='new user', password="test")
             ))

class CategoriesAPI(TestSetup):

    def test_getting_items_by_category(self):
        tester = app.test_client(self)
        register = tester.post(
            'api/user/new',
             data=dict(username='new user', email='e@yahoo.com', password='test')
             )
        token = json.loads(register.data)['token']
        response1 = tester.post(
            f'api/item/new?token={token}',
             data=dict(name='new item', description='test description', category='cat', email='e@yahoo.com', deposit=1.00, overdue_charge=1.00)
             )
        self.assertEqual(response1.status_code, 200)
        response2 = tester.get("/api/categories/cat", content_type="html/text")
        self.assertIn(b'new item', response2.data)

class BookingsAPI(TestSetup):

    def test_request_booking(self):
        tester = app.test_client(self)
        register = tester.post(
            'api/user/new',
             data=dict(username='new user', email='e@yahoo.com', password='test')
             )
        token = json.loads(register.data)['token']
        tester.post(
            f'api/item/new?token={token}',
             data=dict(name='new item', description='test description', category='cat', deposit=1.00, overdue_charge=1.00)
             )
        return_date = (date.today() + timedelta(days = 5))
        bytes_return_date = (str(return_date).encode())
        response = tester.post(
            f'api/booking/new?token={token}',
             data=dict(item_id=1, return_by=return_date)
             )
        self.assertIn(bytes_return_date, response.data)

    def test_get_booking_requests(self):
        tester = app.test_client()
        register = tester.post(
            'api/user/new',
             data=dict(username='new user', email='e@yahoo.com', password='test')
             )
        token = json.loads(register.data)['token']
        tester.post(
            f'api/item/new?token={token}',
             data=dict(name='new item', description='test description', category='cat', deposit=1.00, overdue_charge=1.00)
             )
        return_date = (date.today() + timedelta(days = 5))
        tester.post(
            f'api/booking/new?token={token}',
             data=dict(item_id=1, return_by=return_date)
             )
        return_date = (date.today() + timedelta(days = 5)).strftime("%d/%m/%Y")
        bytes_return_date = (str(return_date).encode())
        response = tester.get(
            f'api/booking/requests?token={token}',
            content_type='html/text'
        )
        self.assertIn(bytes_return_date, response.data)

    def test_get_bookings_confirmed(self):
        tester = app.test_client()
        register = tester.post(
            'api/user/new',
             data=dict(username='new user', email='e@yahoo.com', password='test')
             )
        token = json.loads(register.data)['token']
        tester.post(
            f'api/item/new?token={token}',
             data=dict(name='new item', description='test description', category='cat', deposit=1.00, overdue_charge=1.00)
             )
        return_date = (date.today() + timedelta(days = 5))
        tester.post(
            f'api/booking/new?token={token}',
             data=dict(item_id=1, return_by=return_date)
             )
        return_date = (date.today() + timedelta(days = 5)).strftime("%d/%m/%Y")
        bytes_return_date = (str(return_date).encode())
        tester.patch(
            f'api/booking/1?token={token}',
            data=dict(confirmed=True)
        )
        response = tester.get(
            f'api/booking/confirmed?token={token}',
            content_type='html/text'
        )
        self.assertIn(bytes_return_date, response.data)

    def test_reject_booking(self):
        tester = app.test_client()
        # register a user and get token
        register = tester.post(
            'api/user/new',
             data=dict(username='new user', email='e@yahoo.com', password='test')
             )
        token = json.loads(register.data)['token']
        # add an item to db
        tester.post(
            f'api/item/new?token={token}',
             data=dict(name='new item', description='test description', category='cat', deposit=1.00, overdue_charge=1.00)
             )
        return_date = (date.today() + timedelta(days = 5))
        # request a booking
        tester.post(
            f'api/booking/new?token={token}',
             data=dict(item_id=1, return_by=return_date)
             )
        # reject a booking
        tester.delete(
            f'api/booking/1?token={token}',
            content_type = "html/text"
        )
        # get all booking requests
        response = tester.get(
            f'api/booking/requests?token={token}',
            content_type='html/text'
        )
        self.assertEqual(response.data, b'[]\n')

    def test_get_my_bookings(self):
        tester = app.test_client()
        # register a user and get token
        register = tester.post(
            'api/user/new',
             data=dict(username='new user', email='e@yahoo.com', password='test')
             )
        token = json.loads(register.data)['token']
        # add an item to db
        tester.post(
            f'api/item/new?token={token}',
             data=dict(name='new item', description='test description', category='cat', deposit=1.00, overdue_charge=1.00)
             )
        return_date = (date.today() + timedelta(days = 5))
        # request a booking
        tester.post(
            f'api/booking/new?token={token}',
             data=dict(item_id=1, return_by=return_date)
             )
        # confirm booking
        tester.patch(
            f'api/booking/1?token={token}',
            data=dict(confirmed=True)
        )
        response = tester.get(
            f'api/bookings?token={token}',
            content_type='html/text'
        )
        self.assertIn(b'"confirmed":true',response.data )
