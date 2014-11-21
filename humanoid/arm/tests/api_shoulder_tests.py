from unittest import TestCase
from salvius import app


class ApiShoulderTests(TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()

    def test_get_shoulder(self):
        url = "/api/arms/0/shoulder/"
        response = self.app.get(url, follow_redirects=True)

        print(response.data.decode())

        self.assertTrue('href": "' + url in response.data.decode())
        self.assertTrue("orthogonal" in response.data.decode())

    def test_patch_shoulder(self):
        """
        Test that data can be patched to a shoulder.
        """
        data = '{"rotation": -50}'
        url = "/api/arms/0/shoulder/"
        content_type = "application/json"

        response = self.app.patch(url, data=data, content_type=content_type)

        self.assertTrue("rotation" in response.data.decode())
        self.assertTrue("-50" in response.data.decode())
