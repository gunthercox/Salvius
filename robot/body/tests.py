from unittest import TestCase, TestSuite, TextTestRunner
from ..head import Head
from ..arm import Arm
from ..leg import Leg
from .__init__ import Body

class Tests(TestCase):

    def test_set_head(self):
        body = Body()
        head = Head()
        body.set_head(head)

        self.assertEqual(body.head, head)

    def test_add_arm(self):
        body = Body()
        arm = Arm()
        body.add_arm(arm)

        self.assertEqual(len(body.arms), 1)

    def test_add_leg(self):
        body = Body()
        leg = Leg()
        body.add_leg(leg)

        self.assertEqual(len(body.legs), 1)
