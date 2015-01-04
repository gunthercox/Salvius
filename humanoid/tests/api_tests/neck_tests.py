from unittest import TestCase
from salvius import app

from humanoid.neck import Neck


class ApiTests(TestCase):

    def setUp(self):
        app.config["TESTING"] = True
        self.app = app.test_client()

    def test_get_neck(self):
        response = self.app.get("/neck/", follow_redirects=True)
        self.assertEqual(405, response.status_code)

    def test_patch_neck(self):
        # TODO
        self.assertTrue(True)
