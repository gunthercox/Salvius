from unittest import TestCase
from salvius import app


class BaseTestCase(TestCase):

    def setUp(self):
        app.config["TESTING"] = True
        self.app = app.test_client()
