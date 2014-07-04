from unittest import TestCase, TestSuite, TextTestRunner
from .shoulder import Shoulder

class Tests(TestCase):
    def test_finger(self):
        assert True

    def test_wrist(self):
        assert True

    def test_elbow(self):
        assert True

    def test_shoulder_reset(self):
        shoulder = Shoulder()

        shoulder.rotate(-10)
        shoulder.extend(10)

        shoulder.reset()

        self.assertEqual(shoulder.get_rotation(), 0)
        self.assertEqual(shoulder.get_angle(), 0)
