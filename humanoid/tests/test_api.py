from .base_test_case import BaseTestCase


class ApiTests(BaseTestCase):

    def test_invalid_JSON(self):
        """
        Test status code 405 from improper JSON on post to raw.
        """
        response = self.app.post("/",
                                 data="not a json",
                                 content_type="application/json")
        self.assertEqual(response.status_code, 405)

    def test_get_robot(self):
        response = self.app.get("/", follow_redirects=True)
        self.assertTrue("fingers" in response.data.decode())
        self.assertTrue("knee" in response.data.decode())
