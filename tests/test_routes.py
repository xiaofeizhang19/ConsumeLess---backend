from tests.setup import TestSetup
from consumeless import app, db

class RouteRoot(TestSetup):

    def test_redirect(self):
        tester = app.test_client(self)
        response = tester.get('/', content_type='html/text')
        self.assertEqual(response.status_code, 302)

class RouteApiItemIndex(TestSetup):

    def test_item_index(self):
        tester = app.test_client(self)
        response = tester.get('/api/item/index', content_type='html/text')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
