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

class RouteAPIItemID(TestSetup):

    def test_item_1(self):
        tester = app.test_client(self)
        response = tester.get('/api/item/1', content_type='html/text')
        self.assertEqual(response.status_code, 404)

class RouteAPIUserID(TestSetup):

    def test_user_1(self):
        tester = app.test_client(self)
        response = tester.get('/api/user/1', content_type='html/text')
        self.assertEqual(response.status_code, 404)

class RouteAPICategoryIndex(TestSetup):

    def test_category_index(self):
        tester = app.test_client(self)
        response = tester.get("/api/categories/index", content_type="html/text")
        self.assertEqual(response.status_code, 200)
