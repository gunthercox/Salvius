from unittest import TestCase

from humanoid.leg.hip import Hip
from humanoid.leg.knee import Knee
from humanoid.leg.ankle import Ankle


class HipTests(TestCase):

    def test_hip_rotate(self):
        hip = Hip()
        hip.rotate(-20)

        self.assertEqual(hip.rotation, -20)

    def test_hip_extend(self):
        hip = Hip()
        hip.slant(10)

        self.assertEqual(hip.angle, 10)


class KneeTests(TestCase):

    def test_knee_move(self):
        knee = Knee()
        knee.move(-20)

        self.assertEqual(knee.angle, -20)


class AnkleTests(TestCase):

    def test_ankle_rotate(self):
        ankle = Ankle()
        ankle.rotate(5)

        self.assertEqual(ankle.rotation, 5)

    def test_ankle_elevate(self):
        ankle = Ankle()
        ankle.elevate(6)

        self.assertEqual(ankle.elevation, 6)

    def test_ankle_move(self):
        ankle = Ankle()
        ankle.slant(7)

        self.assertEqual(ankle.angle, 7)
