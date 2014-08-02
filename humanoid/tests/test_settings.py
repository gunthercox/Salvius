from unittest import TestCase
from flask import json, jsonify
from salvius import app


class SettingsTest(TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()

    def test_get_settings(self):
        response = self.app.get("/api/settings", follow_redirects=True)

        self.assertTrue("{" in response.data.decode())
        self.assertTrue("}" in response.data.decode())
