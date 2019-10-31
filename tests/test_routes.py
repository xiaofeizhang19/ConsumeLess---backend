import os
import sys
topdir = os.path.join(os.path.dirname(__file__), "..")
sys.path.append(topdir)
os.environ['APP_SETTINGS']='config.TestingConfig'
from consumeless import app, db

import unittest

class BasicTestCase(unittest.TestCase):

    def setUp(self):
        db.create_all()

    def test_index(self):
        tester = app.test_client(self)
        response = tester.get('/', content_type='html/text')
        self.assertEqual(response.status_code, 302)

class AnotherTestCase(unittest.TestCase):

    def test_item_index(self):
        tester = app.test_client(self)
        response = tester.get('/api/item/index', content_type='html/text')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b'[]\n')


if __name__ == '__main__':
    unittest.main()
