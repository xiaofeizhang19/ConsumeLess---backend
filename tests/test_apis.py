from datetime import datetime
from tests.setup import TestSetup
from consumeless import app, db
from models import Item

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
