from unittest import TestCase
from salvius import app


class SettingsTest(TestCase):

    def setUp(self):
        import os

        # If a settings file does not exist then create one
        if not os.path.isfile("settings.db"):
            content = '{"legs": [{"leg": {"id": 0}}, {"leg": {"id": 1}}]}'
            test = open("settings.db", "w+")
            test.write(content)
            test.close()

        app.config["TESTING"] = True
        self.app = app.test_client()

    def test_get_settings(self):
        response = self.app.get("/settings/", follow_redirects=True)

        self.assertTrue("{" in response.data.decode())
        self.assertTrue("}" in response.data.decode())

    def test_patch_settings(self):
        data = '{"test": true}'
        url = "/settings/"
        content_type = "application/json"

        response = self.app.patch(url, data=data, content_type=content_type)

        # Clean up the test key afterward
        self.app.delete(url, data=data, content_type=content_type)

        self.assertTrue('test": true' in response.data.decode())

    def test_delete_settings(self):
        data = '{"test": true}'
        url = "/settings/"
        content_type = "application/json"

        self.app.patch(url, data=data, content_type=content_type)

        response = self.app.delete(url, data=data, content_type=content_type)

        print(response.data.decode())

        self.assertFalse('test": true' in response.data.decode())
