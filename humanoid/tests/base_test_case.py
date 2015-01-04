from unittest import TestCase
from salvius import app


class BaseTestCase(TestCase):

    def setUp(self):
        from humanoid.robotics import Robot
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
