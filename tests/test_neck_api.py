from .base_test_case import BaseTestCase


class ApiTests(BaseTestCase):

    def test_get_neck(self):
        response = self.app.get("/neck/", follow_redirects=True)
        self.assertEqual(405, response.status_code)

    def test_patch_neck(self):
        # TODO
        self.assertTrue(True)
