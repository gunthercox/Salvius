from unittest import TestCase

from humanoid.arm.shoulder import Shoulder
from humanoid.arm.elbow import Elbow
from humanoid.arm.wrist import Wrist
from humanoid.arm.hand import Hand, Finger


class ShoulderTests(TestCase):

    def test_shoulder_rotate(self):
        shoulder = Shoulder(0)
        shoulder.rotate(-10)

        self.assertEqual(shoulder.rotation, -10)

    def test_shoulder_extend(self):
        shoulder = Shoulder(0)
        shoulder.slant(10)

        self.assertEqual(shoulder.angle, 10)


class ElbowTests(TestCase):

    def test_elbow_move(self):
        elbow = Elbow(0)
        elbow.move(-20)

        self.assertEqual(elbow.angle, -20)


class WristTests(TestCase):

    def test_wrist_move(self):
        wrist = Wrist(0)

        wrist.rotate(5)
        wrist.elevate(6)
        wrist.slant(7)

        self.assertEqual(wrist.rotation, 5)
        self.assertEqual(wrist.elevation, 6)
        self.assertEqual(wrist.angle, 7)


class HandTests(TestCase):

    def test_add_finger(self):
        hand = Hand()

        self.assertEqual(len(hand.fingers), 0)


class FingerTests(TestCase):

    def test_finger_move(self):
        finger = Finger(0, 0)
        finger.move(-30)

        self.assertEqual(finger.tension, -30)
