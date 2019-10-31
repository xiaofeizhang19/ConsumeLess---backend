import os
import sys
topdir = os.path.join(os.path.dirname(__file__), "..")
sys.path.append(topdir)
os.environ['APP_SETTINGS']='config.TestingConfig'
from consumeless import app, db
import unittest

class TestSetup(unittest.TestCase):
    def setUp(self):
        db.drop_all()
        db.create_all()
