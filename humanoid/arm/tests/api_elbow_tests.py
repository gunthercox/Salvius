from unittest import TestCase
from salvius import app


class ApiElbowTests(TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()

    def test_get_elbow(self):
        url = "/arms/0/elbow/"
        response = self.app.get(url, follow_redirects=True)

        self.assertTrue('href": "' + url in response.data.decode())
        self.assertTrue("hinge" in response.data.decode())
        self.assertTrue("limits" in response.data.decode())

    def test_patch_elbow(self):
        """
        Test that data can be patched to an elbow.
        """
        data = '{"angle": -20}'
        url = "/arms/0/elbow/"
        content_type = "application/json"

        response = self.app.patch(url, data=data, content_type=content_type)

        self.assertTrue("angle" in response.data.decode())
        self.assertTrue("-20" in response.data.decode())
