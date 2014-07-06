from unittest import TestCase, TestSuite, TextTestRunner
from ..arm import Arm
from .__init__ import Body

class Tests(TestCase):

    def test_add_arm(self):
        body = Body()
        arm = Arm()
        body.add_arm(arm)

        self.assertTrue(len(body.arms) == 1)
