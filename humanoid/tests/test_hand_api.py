from .base_test_case import BaseTestCase


class ApiFingerTests(BaseTestCase):

    def test_get_thumb(self):
        response = self.app.get("/arms/index_finger/thumb/", follow_redirects=True)
        self.assertEqual(405, response.status_code)

    def test_patch_finger(self):
        # TODO Mock models are required before testing can be done without hardware
        self.assertTrue(True)


class ApiThumbTests(BaseTestCase):

    def test_get_thumb(self):
        response = self.app.get("/arms/right_thumb/thumb/", follow_redirects=True)
        self.assertEqual(405, response.status_code)

    def test_patch_thumb(self):
        # TODO Mock models are required before testing can be done without hardware
        self.assertTrue(True)
