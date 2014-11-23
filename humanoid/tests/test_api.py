from unittest import TestCase
from salvius import app


class ApiTests(TestCase):

    def setUp(self):
        from humanoid import Robot
        import os

        # If a settings file does not exist then create one
        if not os.path.isfile("settings.db"):
            content = '{"legs": [{"leg": {"id": 0}}, {"leg": {"id": 1}}]}'
            test = open("settings.db", "w+")
            test.write(content)
            test.close()

        app.config["TESTING"] = True
        app.config["ROBOT"] = Robot()
        self.app = app.test_client()

    def test_invalid_JSON(self):
        """
        Test status code 405 from improper JSON on post to raw.
        """
        response = self.app.post("/api/",
                                 data="not a json",
                                 content_type="application/json")
        self.assertEqual(response.status_code, 405)

    def test_get_robot(self):
        response = self.app.get("/api/", follow_redirects=True)
        self.assertTrue('"name": "Salvius"' in response.data.decode())

    def test_get_robot(self):
        response = self.app.get("/api/", follow_redirects=True)
        self.assertTrue("fingers" in response.data.decode())
        self.assertTrue("torso" in response.data.decode())
        self.assertTrue("knee" in response.data.decode())
