from unittest import TestCase, TestSuite, TextTestRunner
from ..arm import Arm
from .__init__ import Body

class Tests(TestCase):

    def test_add_arm(self):
        body = Body()
        arm = Arm()
        body.addArm(arm)

        self.assertTrue(len(body.list_arms()) == 1)
