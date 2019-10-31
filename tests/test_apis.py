from tests.setup import TestSetup
from consumeless import app, db
from models import Item

class RouteRoot(TestSetup):

    def test_item_1_populated(self):
        newItem = Item(name = 'test',
                    description = "testing",
                    category = 'test',
                    email = 'test@gmail.com',
                    deposit = 1.00,
                    overdue_charge = 1.00)
        expected_output = b'{"category":"test","deposit":"1.0","description":"testing","email":"test@gmail.com","id":1,"name":"test","overdue_charge":"1.0"}\n'
        db.session.add(newItem)
        tester = app.test_client(self)
        response = tester.get('api/item/1', content_type='html/text')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, expected_output)
