from unittest import TestCase

from robot.head import Head
from robot.body import Body
from robot.arm import Arm
from robot.leg import Leg


class Tests(TestCase):

    def test_set_head(self):
        body = Body()
        head = Head()
        body.set_head(head)

        self.assertEqual(body.head, head)

    def test_add_arm(self):
        body = Body()
        arm = body.new_arm()

        self.assertEqual(len(body.arms), 1)

    def test_add_leg(self):
        body = Body()
        leg = Leg()
        body.add_leg(leg)

        self.assertEqual(len(body.legs), 1)
