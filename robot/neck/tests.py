from unittest import TestCase
from robot.head import Head, Neck


class Tests(TestCase):

    def test_set_camera_url(self):
        head = Head()
        url = "http://0.0.0.0:7000/"
        head.set_camera_url(url)

        self.assertEqual(head.get_camera_url(), url)

    def test_neck_add_head(self):
        head = Head()
        neck = Neck()

        neck.set_head(head)

        self.assertEqual(neck.head, head)
