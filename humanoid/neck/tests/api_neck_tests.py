from unittest import TestCase
from salvius import app


class ApiTests(TestCase):

    def setUp(self):
        app.config["TESTING"] = True
        self.app = app.test_client()

    def test_get_neck(self):
        response = self.app.get("/neck/", follow_redirects=True)
        self.assertTrue("joint_type" in response.data.decode())
