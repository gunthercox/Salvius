from unittest import TestCase
from salvius import app


class ApiTests(TestCase):

    def setUp(self):
        from humanoid import Robot
        app.config["TESTING"] = True
        app.config["ROBOT"] = Robot()
        self.app = app.test_client()

    def test_finger_count(self):
        response = self.app.get("/arms/0/hand/fingers", follow_redirects=True)
        data = response.data.decode()

        self.assertEqual(data.count('href'), 4)

    def test_patch_finger(self):
        """
        Test that data can be patched to fingers.
        """
        data = '{"tension": 2}'
        url = "/arms/0/hand/fingers/0/"

        response = self.app.patch(url, data=data, content_type='application/json')

        print(response.data.decode())

        self.assertTrue("tension" in response.data.decode())
        self.assertTrue("2" in response.data.decode())

    def test_patch_one_field_thumb(self):
        """
        Test that data can be patched to a thumb.
        """
        data = '{"tension": 4}'
        url = "/arms/0/hand/thumb/"

        response = self.app.patch(url, data=data, content_type='application/json')

        self.assertTrue("tension" in response.data.decode())
        self.assertTrue("4" in response.data.decode())
