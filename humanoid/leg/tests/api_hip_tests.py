from unittest import TestCase
from salvius import app


class HipApiTests(TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()

    def test_get_hip(self):
        url = "/api/legs/0/hip/"
        response = self.app.get(url, follow_redirects=True)

        self.assertTrue("/api/legs/" in response.data.decode())

    def test_patch_hip(self):
        """
        Test that two fields can be patched to a hip.
        """
        data = u'{"angle": 2}'
        url = "/api/legs/0/hip/"
        content_type = "application/json"

        response = self.app.patch(url, data=data, content_type=content_type)

        self.assertTrue('angle": 2' in response.data.decode())

    def test_one_invalid_field_hip(self):
        """
        Test that patching one valid and one invalid field fails.
        """
        data = '{"bogus": 2, "angle": 9}'
        url = "/api/legs/0/hip/"
        content_type = "application/json"

        response = self.app.patch(url, data=data, content_type=content_type)

        self.assertTrue("405" in response.data.decode())
