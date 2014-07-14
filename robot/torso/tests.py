from unittest import TestCase

from robot.torso import Torso


class Tests(TestCase):

    def test_set_rotaton(self):
        torso = Torso()

        torso.move(25)

        self.assertEqual(torso.rotation, 25)
