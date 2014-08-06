from unittest import TestCase

from humanoid.neck import Neck
from humanoid.torso import Torso
from humanoid.body import Body
from humanoid.arm import Arm
from humanoid.leg import Leg


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
