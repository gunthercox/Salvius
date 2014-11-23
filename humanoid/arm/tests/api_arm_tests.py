from unittest import TestCase
from salvius import app


class ApiArmTests(TestCase):

    def setUp(self):
        from humanoid import Robot
        app.config["TESTING"] = True
        app.config["ROBOT"] = Robot()
        self.app = app.test_client()

    def test_get_arms(self):
        response = self.app.get("/arms/", follow_redirects=True)
        self.assertTrue("fingers" in response.data.decode())
        self.assertTrue("shoulder" in response.data.decode())
        self.assertTrue("torso" not in response.data.decode())
        self.assertTrue("knee" not in response.data.decode())

    def test_get_one_arm(self):
        response = self.app.get("/arms/0", follow_redirects=True)
        self.assertTrue("fingers" in response.data.decode())
        self.assertTrue("shoulder" in response.data.decode())
        self.assertTrue("torso" not in response.data.decode())
        self.assertTrue("knee" not in response.data.decode())
