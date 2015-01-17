class Arduino(object):
    """
    This object represents an arduino board.
    It contains methods that will allow you to interact
    with an arduino controller through a serial connection.
    """

    def __init__(self, name):
        self.name = name
        self.port = None

        ports = self.list_device_ports()

        for port in ports:
            print port[0]
            data = self.read(port[0])
            if name in data:
                self.port = port[0]

        # If no maching port could be found, thrown an exception
        if not self.port:
            raise UnboundLocalError("A port connected to an arduino board named \"%s\" could not be found." % (name))

    def list_device_ports(self):
        """
        Returns a list of usb ports that could possible be connected to arduino
        boards.
        """
        from serial.tools import list_ports

        ports = list(list_ports.grep('/dev/ttyUSB*|/dev/ttyACM*'))

        return ports

    def clean(self, line, ending):
        if line.endswith(ending):
            return line[:-len(ending)]
        return line

    def read(self, port):
        import serial

        lines = []

        connection = serial.Serial(port, 9600, timeout=1)
        connection.write(":")
        line_data = connection.readlines()
        connection.close()

        print line_data

        for line in line_data:
            cleaned_line = self.clean(line, "\r\n")
            lines.append(cleaned_line)

        return lines

    def write(self, text):
        import serial

        lines = []

        connection = serial.Serial(self.port, 9600, timeout=1)
        connection.write(text)
        line_data = connection.readlines()
        connection.close()

        for line in line_data:
            cleaned_line = self.clean(line, "\r\n")
            lines.append(cleaned_line)

            print line

        return lines
