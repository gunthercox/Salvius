from unittest import TestCase
from zorg.test import MockAdaptor
from salvius.hbridge import HBridge


class HBridgeTestCase(TestCase):

    def setUp(self):
        super(HBridgeTestCase, self).setUp()

        self.connection = MockAdaptor({
            'methods': ['hbridge_write']
        })
        self.options = {}

        self.driver = HBridge(self.options, self.connection)

    def test_command_method_exists(self):
        """
        Check that each command listed has a corresponding
        method on the driver class.
        """
        for command in self.driver.commands:
            self.assertIn(command, dir(self.driver))

    def test_turn_off(self):
        self.driver.turn_off()
        self.assertEqual(self.driver.state, 0)

    def test_rotate_clockwise(self):
        value = self.driver.rotate_clockwise()
        self.assertEqual(self.driver.state, 1)

    def test_rotate_counterclockwise(self):
        value = self.driver.rotate_counterclockwise()
        self.assertEqual(self.driver.state, -1)
