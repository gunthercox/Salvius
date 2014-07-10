from unittest import TestCase

from robot.arm.shoulder import Shoulder
from robot.arm.elbow import Elbow
from robot.arm.wrist import Wrist
from robot.arm.hand import Hand, Finger


class ShoulderTests(TestCase):

    def test_shoulder_reset(self):
        shoulder = Shoulder()

        shoulder.rotate(-10)
        shoulder.extend(10)

        shoulder.reset()

        self.assertEqual(shoulder.get_rotation(), 0)
        self.assertEqual(shoulder.get_angle(), 0)


class ElbowTests(TestCase):

    def test_elbow_move(self):
        elbow = Elbow()
        elbow.move(-20)

        self.assertEqual(elbow.get_angle(), -20)

    def test_elbow_reset(self):
        elbow = Elbow()
        elbow.move(-20)
        elbow.reset()

        self.assertEqual(elbow.get_angle(), 0)


class WristTests(TestCase):

    def test_wrist_reset(self):
        wrist = Wrist()

        wrist.rotate(5)
        wrist.tilt(6)
        wrist.lean(7)

        wrist.reset()

        print(wrist.get_position())

        self.assertTrue(wrist.get_position() == [0, 0, 0])


class HandTests(TestCase):

    def test_add_finger(self):
        hand = Hand()

        hand.add_finger()
        hand.add_finger()

        self.assertEqual(len(hand.fingers), 2)

    def test_close_hand(self):
        hand = Hand()
        thumb = Finger(0)
        for finger in range(4):
            hand.add_finger()
        hand.set_thumb(thumb)

        hand.close()

        self.assertEqual(hand.fingers[0].get_position(), 100)
        self.assertEqual(hand.thumb.get_position(), 100)


class FingerTests(TestCase):

    def test_finger_move(self):
        finger = Finger(0)
        finger.move(-30)

        self.assertEqual(finger.get_position(), -30)

