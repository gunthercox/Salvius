class Arduino(object):
    """
    This object represents an arduino board.
    It contains methods that will allow you to interact
    with an arduino controller through a serial connection.
    """

    def __init__(self, port):
        self.port = port

    def list_device_ports(self):
        """
        Returns a list of usb ports that could possibly be
        connected to arduino boards.
        """
        from serial.tools import list_ports

        ports = list(list_ports.grep('/dev/ttyUSB*|/dev/ttyACM*'))

        return ports

    def clean(self, line, ending):
        if line.endswith(ending):
            return line[:-len(ending)]
        return line

    def read(self, port=None):
        import serial

        if not port:
            port = self.port

        connection = serial.Serial(port, 9600, timeout=1)
        lines = connection.readlines()
        connection.close()

        return lines

    def write(self, text):
        import serial

        connection = serial.Serial(self.port, 9600, timeout=1)
        connection.write(text)
        connection.close()

        print "self.read -->", self.read()
