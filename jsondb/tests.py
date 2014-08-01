from unittest import TestCase
from jsondb.db import Database


class Tests(TestCase):

    def setUp(self):
        content = "{\"image_url\": \"http://sky.net/image.jpg\", \"ip\": \"http://192.168.1.337\"}"
        test = open("test.db", "w+")
        test.write(content)

    def tearDown(self):
        import os
        os.remove("test.db")

    def test_assign_key_value_pair(self):
        db = Database("test.db")
        db.data(key="cool", value="robot")

        self.assertEqual(db.data(key="cool"), "robot")

    def test_assign_dictionary(self):
        db = Database("test.db")
        d = {
            "id": "123456",
            "arduino_ip": "xxxxxx"
        }
        db.data(dictionary=d)

        self.assertTrue("id" in db.data())
        self.assertEqual(db.data(key="arduino_ip"), "xxxxxx")
