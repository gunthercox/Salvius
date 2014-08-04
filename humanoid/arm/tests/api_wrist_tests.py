from unittest import TestCase
from salvius import app


class ApiWristTests(TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()

    def test_get_wrist(self):
        url = "/api/robot/body/arms/0/wrist/"
        response = self.app.get(url, follow_redirects=True)

        self.assertTrue('href": "' + url in response.data.decode())
        self.assertTrue("articulated" in response.data.decode())

    def test_patch_wrist(self):
        """
        Test that data can be patched to a wrist.
        """
        data = '{"rotation": 2, "angle": -20}'
        url = "/api/robot/body/arms/0/wrist/"
        content_type = "application/json"

        response = self.app.patch(url, data=data, content_type=content_type)

        self.assertTrue("rotation" in response.data.decode())
        self.assertTrue("angle" in response.data.decode())
        self.assertTrue("-20" in response.data.decode())
