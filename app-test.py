from app import app

import unittest


class BasicTestCase(unittest.TestCase):

    def test_index(self):
        tester = app.test_client(self)
        response = tester.get('/', content_type='html/text')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b'Hello World!')

class AnotherTestCase(unittest.TestCase):

    def test_item_index(self):
        tester = app.test_client(self)
        response = tester.get('/api/item/index', content_type='html/text')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b'[]\n')

if __name__ == '__main__':
    unittest.main()
