from unittest import TestCase

from robot.neck import Neck
from robot.torso import Torso
from robot.body import Body
from robot.arm import Arm
from robot.leg import Leg


class Tests(TestCase):

    def test_neck_exists(self):
        body = Body()

        self.assertEqual(type(body.neck), Neck)

    def test_torso_exists(self):
        body = Body()

        self.assertEqual(type(body.torso), Torso)

    def test_add_arm(self):
        body = Body()
        arm = body.new_arm()

        self.assertEqual(len(body.arms), 1)

    def test_add_leg(self):
        body = Body()
        leg = body.new_leg()

        self.assertEqual(len(body.legs), 1)
