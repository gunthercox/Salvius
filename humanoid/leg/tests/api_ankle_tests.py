from unittest import TestCase
from salvius import app


class AnkleApiTests(TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()

    def test_get_ankle(self):
        url = "/legs/0/ankle/"
        response = self.app.get(url, follow_redirects=True)

        self.assertTrue("/legs/" in response.data.decode())

    def test_patch_two_fields_ankle(self):
        """
        Test that two fields can be patched to an ankle.
        """
        data = u'{"rotation": 2, "elevation": 9}'
        url = "/legs/0/ankle/"
        content_type = "application/json"

        response = self.app.patch(url, data=data, content_type=content_type)

        self.assertTrue("rotation\": 2" in response.data.decode())
        self.assertTrue("elevation\": 9" in response.data.decode())

    def test_one_invalid_field_ankle(self):
        """
        Test that patching one valid and one invalid field fails.
        """
        data = '{"position": 2, "angle": 9}'
        url = "/legs/0/ankle/"
        content_type = "application/json"

        response = self.app.patch(url, data=data, content_type=content_type)

        self.assertTrue("405" in response.data.decode())
