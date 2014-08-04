from unittest import TestCase
from salvius import app


class ApiTests(TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()

    def test_invalid_JSON(self):
        """
        Test status code 405 from improper JSON on post to raw.
        """
        response = self.app.post("/api/robot/",
                                 data="not a json",
                                 content_type="application/json")
        self.assertEqual(response.status_code, 405)

    def test_get_robot(self):
        response = self.app.get("/api/robot", follow_redirects=True)
        self.assertTrue('"name": "Salvius"' in response.data.decode())
