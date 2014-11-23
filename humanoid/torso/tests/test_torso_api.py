from unittest import TestCase
from flask import json, jsonify
from salvius import app


class TorsoApiTest(TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()

    def test_get_torso(self):
        """
        Test that torso data can be retrieved.
        """
        url = "/torso/"
        response = self.app.get(url, follow_redirects=True)
        self.assertTrue("href" in response.data.decode())
        self.assertTrue("pivot" in response.data.decode())

    def test_patch_torso(self):
        """
        Test that data can be patched to the torso.
        """
        url = "/torso/"
        data = '{"rotation": 2}'
        content_type = "application/json"

        response = self.app.patch(url, data=data, content_type=content_type)

        self.assertTrue("rotation" in response.data.decode())
        self.assertTrue("2" in response.data.decode())

    def test_invalid_field_cannot_patch_torso(self):
        """
        Test that invalid data cannot be patched to the torso.
        """
        url = "/torso/"
        data = '{"rotation": 2, "invalid": "yes"}'
        content_type = "application/json"

        response = self.app.patch(url, data=data, content_type=content_type)

        self.assertTrue("405" in response.data.decode())
