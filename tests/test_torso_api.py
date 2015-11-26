from .base_test_case import BaseTestCase


class TorsoApiTest(BaseTestCase):

    def test_get_torso(self):
        """
        Test that torso data can be retrieved.
        """
        url = "/torso/"
        response = self.app.get(url, follow_redirects=True)
        self.assertEqual(405, response.status_code)

    def test_patch_torso(self):
        """
        Test that data can be patched to the torso.
        """
        url = "/torso/"
        data = '{"rotate": 2}'
        content_type = "application/json"

        response = self.app.patch(url, data=data, content_type=content_type)

        self.assertTrue("rotate" in response.data.decode())
        self.assertTrue("2" in response.data.decode())
