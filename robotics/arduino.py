class Arduino(object):
    """
    This object represents an arduino board.
    It contains methods that will allow you to interact
    with an arduino controller through a serial connection.
    """

    def __init__(self, port, baudrate=9600):
        self.port = port
        self.baudrate = baudrate

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

        connection = serial.Serial(port, self.baudrate, timeout=1)
        lines = connection.readlines()
        connection.close()

        return lines

    def write(self, text):
        import serial

        # Ensure that the text is a string and not unicode
        text = str(text).encode("ascii") + "\n"

        connection = serial.Serial()
        connection.port = self.port
        connection.baudrate = self.baudrate
        connection.timeout = 1.5
        connection.parity = serial.PARITY_NONE
        connection.stopbits = serial.STOPBITS_TWO
        connection.bytesize = serial.EIGHTBITS
        connection.xonxoff = False
        connection.rtscts = False
        connection.dsrdtr = False

        connection.open()

        print connection.readline()

        connection.write(text)
        connection.close()

        #print "self.read -->", self.read()
