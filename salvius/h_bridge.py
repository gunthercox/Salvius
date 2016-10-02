from zorg.driver import Driver
from zorg_firmata import Firmata


class ArduinoServoHBridgeController(Firmata):
    """
    An adaptor class that allows an h-bridge driver to
    control a servo based h-bridge connected to an Arduino.
    """

    def __init__(self, options):
        super(ArduinoServoHBridgeController, self).__init__(options)

        self.servo_angle_map = options.get('servo_angle_map', {
            -1: 50,
            0: 40,
            1: 32
        })

    def hbridge_write(self, options, state):
        # Convert the h-bridge state to a servo angle
        pin = options.get('pin')
        angle = self.servo_angle_map[state]
        self.servo_write(pin, angle)


class ArduinoRelayHBridgeController(Firmata):
    """
    An adaptor class that allows an h-bridge driver to
    control a relay based h-bridge connected to an Arduino.
    """

    def hbridge_write(self, value):
        pass


class HBridge(Driver):
    """
    A generic h-bridge driver class.
    """

    def __init__(self, options, connection):
        super(HBridge, self).__init__(options, connection)

        self.options = options
        self.state = 0
        self.commands += [
            'turn_off',
            'rotate_clockwise',
            'rotate_counterclockwise'
        ]

    def turn_off(self):
        """
        Turn the h-bridge off.
        """
        self.state = 0
        self.connection.hbridge_write(self.options, 0)

    def rotate_clockwise(self):
        """
        Turn the h-bridge on and set it to spin the motor clockwise.
        """
        self.state = 1
        self.connection.hbridge_write(self.options, 1)

    def rotate_counterclockwise(self):
        """
        Turn the h-bridge on and set it to spin the motor counterclockwise.
        """
        self.state = -1
        self.connection.hbridge_write(self.options, -1)
