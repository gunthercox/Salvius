from unittest import TestCase
from humanoid.neck import Neck


class Tests(TestCase):

    def test_rotate_neck(self):
        neck = Neck()
        neck.rotate(-10)

        self.assertEqual(neck.rotation, -10)
