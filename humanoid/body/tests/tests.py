from unittest import TestCase

from humanoid.body import Body
from humanoid.neck import Neck
from humanoid.torso import Torso
from humanoid.arm import Arm
from humanoid.leg import Leg


class Tests(TestCase):

    def test_add_arm(self):
        body = Body()
        arm = body.new_arm()

        self.assertEqual(len(body.arms), 1)
