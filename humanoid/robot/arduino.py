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
            data = self.read(port)
            if name in data:
                self.port = port

        # If no maching port could be found, thrown an exception
        if not self.port:
            raise UnboundLocalError("A port connected to an arduino board named \"%s\" could not be found." % (name))

    def list_device_ports(self):
        from serial.tools import list_ports

        all_ports = list_ports.glob.glob("/dev/tty[A-Za-z]*")
        ports = []

        for port in all_ports:
            if "USB" in port or "ACM" in port:
                ports.append(port)

        return ports

    def clean(self, line, ending):
        if line.endswith(ending):
            return line[:-len(ending)]
        return line

    def read(self, port):
        import serial

        lines = []

        connection = serial.Serial(port, 115200, timeout=1)
        connection.write(" ")
        line_data = connection.readlines()
        connection.close()

        for line in line_data:
            cleaned_line = self.clean(line, "\r\n")
            lines.append(cleaned_line)

        return lines

    def write(self, text):
        import serial

        lines = []

        connection = serial.Serial(self.port, 115200, timeout=1)
        connection.write(text)
        line_data = connection.readlines()
        connection.close()

        for line in line_data:
            cleaned_line = self.clean(line, "\r\n")
            lines.append(cleaned_line)

        return lines
