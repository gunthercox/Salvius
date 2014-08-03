from unittest import TestCase
from flask import json
from salvius import app


class Test(TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()

    def test_invalid_JSON(self):
        """
        Test status code 405 from improper JSON on post to raw.
        """
        response = self.app.post('/api/robot/',
                                 data="not a json",
                                 content_type='application/json')
        self.assertEqual(response.status_code, 405)

    def test_get_robot(self):
        response = self.app.get("/api/robot", follow_redirects=True)
        self.assertTrue('"name": "Salvius"' in response.data.decode())

    def test_get_body(self):
        response = self.app.get("/api/robot/body", follow_redirects=True)
        self.assertTrue("fingers" in response.data.decode())
        self.assertTrue("torso" in response.data.decode())
        self.assertTrue("knee" in response.data.decode())

    def test_get_neck(self):
        response = self.app.get("/api/robot/body/neck", follow_redirects=True)
        self.assertTrue("joint_type" in response.data.decode())

    def test_get_arms(self):
        response = self.app.get("/api/robot/body/arms", follow_redirects=True)
        self.assertTrue("fingers" in response.data.decode())
        self.assertTrue("shoulder" in response.data.decode())
        self.assertTrue("torso" not in response.data.decode())
        self.assertTrue("knee" not in response.data.decode())

    def test_get_one_arm(self):
        response = self.app.get("/api/robot/body/arms/0", follow_redirects=True)
        self.assertTrue("fingers" in response.data.decode())
        self.assertTrue("shoulder" in response.data.decode())
        self.assertTrue("torso" not in response.data.decode())
        self.assertTrue("knee" not in response.data.decode())

    def test_finger_count(self):
        response = self.app.get("/api/robot/body/arms/0/hand/fingers", follow_redirects=True)
        data = response.data.decode()
        print(data)
        self.assertEqual(data.count('href'), 4)

    def test_patch_finger(self):
        """
        Test that data can be patched to fingers.
        """
        data = '{"position": 2}'
        url = "/api/robot/body/arms/0/hand/fingers/0/"

        response = self.app.patch(url, data=data, content_type='application/json')

        self.assertTrue("position" in response.data.decode())
        self.assertTrue("2" in response.data.decode())

    def test_patch_one_field_thumb(self):
        """
        Test that data can be patched to a thumb.
        """
        data = '{"position": 4}'
        url = "/api/robot/body/arms/0/hand/thumb/"

        response = self.app.patch(url, data=data, content_type='application/json')

        self.assertTrue("position" in response.data.decode())
        self.assertTrue("4" in response.data.decode())
