from unittest import TestCase
from salvius import app


class ApiTests(TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()

    def test_get_body(self):
        response = self.app.get("/api/robot/body", follow_redirects=True)
        self.assertTrue("fingers" in response.data.decode())
        self.assertTrue("torso" in response.data.decode())
        self.assertTrue("knee" in response.data.decode())
