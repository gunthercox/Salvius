from unittest import TestCase
from salvius import app


class KneeApiTests(TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()

    def test_get_knee(self):
        url = "/api/legs/0/knee/"
        response = self.app.get(url, follow_redirects=True)

        self.assertTrue("/api/legs/" in response.data.decode())

    def test_patch_knee(self):
        """
        Test that two fields can be patched to a knee.
        """
        data = u'{"angle": 2}'
        url = "/api/legs/0/knee/"
        content_type = "application/json"

        response = self.app.patch(url, data=data, content_type=content_type)

        self.assertTrue('angle": 2' in response.data.decode())

    def test_one_invalid_field_knee(self):
        """
        Test that patching one valid and one invalid field fails.
        """
        data = '{"position": 2, "angle": 9}'
        url = "/api/legs/0/knee/"
        content_type = "application/json"

        response = self.app.patch(url, data=data, content_type=content_type)

        self.assertTrue("405" in response.data.decode())
