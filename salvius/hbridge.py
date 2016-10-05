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

        return state


class ArduinoRelayHBridgeController(Firmata):
    """
    An adaptor class that allows an h-bridge driver to
    control a relay based h-bridge connected to an Arduino.
    """

    def hbridge_write(self, options, state):
        pins = options.get('pins')

        # Turn the h-bridge off
        if state == 0:
            # All relays to the normally open position
            for pin in pins:
                self.digital_write(pin, 0)

        # Rotate motor clockwise
        if state == 1:
            # Set two opposite adjacent pairs of relays to opposite states
            self.digital_write(pins[0], 0)
            self.digital_write(pins[1], 1)
            self.digital_write(pins[2], 0)
            self.digital_write(pins[3], 1)

        # Rotate motor counterclockwise
        if state == -1:
            # Set two opposite adjacent pairs of relays to opposite states
            self.digital_write(pins[0], 1)
            self.digital_write(pins[1], 0)
            self.digital_write(pins[2], 1)
            self.digital_write(pins[3], 0)

        return state


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
        self.turn_off()
        self.state = 1
        self.connection.hbridge_write(self.options, 1)

    def rotate_counterclockwise(self):
        """
        Turn the h-bridge on and set it to spin the motor counterclockwise.
        """
        self.turn_off()
        self.state = -1
        self.connection.hbridge_write(self.options, -1)
