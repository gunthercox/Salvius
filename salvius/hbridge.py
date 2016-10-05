from zorg.driver import Driver
from zorg_gpio import Relay


class HBridge(Driver):
    """
    A h-bridge base class.
    """

    def __init__(self, options, connection):
        super(HBridge, self).__init__(options, connection)

        self.state = 0

        self.commands += [
            'turn_off',
            'rotate_clockwise',
            'rotate_counterclockwise'
        ]

    class RelayException(Exception):

        def __init__(self, value):
            self.value = value

        def __str__(self):
            return repr(self.value)


class RelayHBridge(HBridge):
    """
    A relay h-bridge driver class.
    """

    def __init__(self, options, connection):
        super(RelayHBridge, self).__init__(options, connection)

        self.relays = []
        pins = options.get('pins', [])

        # Raise exception if four pins have not been provided
        if len(pins) != 4:
            raise self.RelayException(
                '{} pins were given when 4 were expected'.format(len(pins))
            )

        for pin in pins:
            relay_options = options.copy()
            relay_options['pin'] = pin
            relay = Relay(relay_options, self.connection)
            self.relays.append(relay)

    def turn_relays_off_if_on(self):
        """
        Turn each relay off only if it is on.
        This prevents unnecessary writes to relays that are already off.
        """
        for relay in self.relays:
            if relay.is_on():
                relay.turn_off()

    def turn_off(self):
        """
        Turn the h-bridge off.
        """
        self.state = 0
        self.turn_relays_off_if_on()

    def rotate_clockwise(self):
        """
        Turn the h-bridge on and set it to spin the motor clockwise.
        """
        self.state = 1

        # Turn any active relays off to prevent a short circuit
        self.turn_relays_off_if_on()

        # Set two opposite adjacent pairs of relays to opposite states
        self.relays[1].turn_on()
        self.relays[3].turn_on()

    def rotate_counterclockwise(self):
        """
        Turn the h-bridge on and set it to spin the motor counterclockwise.
        """
        self.state = -1

        # Turn any active relays off to prevent a short circuit
        self.turn_relays_off_if_on()

        # Set two opposite adjacent pairs of relays to opposite states
        self.relays[0].turn_on()
        self.relays[2].turn_on()


class ServoHBridge(HBridge):
    """
    A servo h-bridge driver class.
    """

    def __init__(self, options, connection):
        super(ServoHBridge, self).__init__(options, connection)

        self.servo_angle_map = options.get('servo_angle_map', {
            -1: 50,
            0: 40,
            1: 32
        })

    def turn_off(self):
        """
        Turn the h-bridge off.
        """
        self.state = 0
        angle = self.servo_angle_map[self.state]
        self.connection.servo_write(self.pin, angle)

    def rotate_clockwise(self):
        """
        Turn the h-bridge on and set it to spin the motor clockwise.
        """
        self.state = 1
        angle = self.servo_angle_map[self.state]
        self.connection.servo_write(self.pin, angle)

    def rotate_counterclockwise(self):
        """
        Turn the h-bridge on and set it to spin the motor counterclockwise.
        """
        self.state = -1
        angle = self.servo_angle_map[self.state]
        self.connection.servo_write(self.pin, angle)
