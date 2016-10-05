from unittest import TestCase
from zorg.test import MockAdaptor
from salvius.hbridge import RelayHBridge, ServoHBridge


class HBridgeTestCase(TestCase):

    def setUp(self):
        super(HBridgeTestCase, self).setUp()

        self.connection = MockAdaptor({
            'methods': ['servo_write', 'digital_write']
        })
        self.options = {}


class RelayHBridgeTestCase(HBridgeTestCase):

    def setUp(self):
        super(RelayHBridgeTestCase, self).setUp()
        self.options['pins'] = [1, 2, 3, 4] 
        self.driver = RelayHBridge(self.options, self.connection)

    def test_command_method_exists(self):
        """
        Check that each command listed has a corresponding
        method on the driver class.
        """
        for command in self.driver.commands:
            self.assertIn(command, dir(self.driver))

    def test_four_pins_not_given(self):
        self.options['pins'] = []
        with self.assertRaises(RelayHBridge.RelayException):
            RelayHBridge(self.options, self.connection)

    def test_turn_off(self):
        self.driver.turn_off()
        self.assertEqual(self.driver.state, 0)

    def test_rotate_clockwise(self):
        value = self.driver.rotate_clockwise()
        self.assertEqual(self.driver.state, 1)

    def test_rotate_counterclockwise(self):
        value = self.driver.rotate_counterclockwise()
        self.assertEqual(self.driver.state, -1)


class ServoHBridgeTestCase(HBridgeTestCase):

    def setUp(self):
        super(ServoHBridgeTestCase, self).setUp()
        self.driver = ServoHBridge(self.options, self.connection)

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
