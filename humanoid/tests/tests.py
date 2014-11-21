from unittest import TestCase
from humanoid import Robot


class Tests(TestCase):

    def test_arms_added(self):
        robot = Robot()

        self.assertEqual(len(robot.arms), 2)
