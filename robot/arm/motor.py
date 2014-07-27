import smbus
import time


# This is a test file to test the i2c stuff in python.
bus = smbus.SMBus(0)
address = 0x60


def bearing255():
    bear = bus.read_byte_data(address, 1)
    return bear


def bearing3599():
    bear1 = bus.read_byte_data(address, 2)
    bear2 = bus.read_byte_data(address, 3)
    bear = (bear1 << 8) + bear2
    bear = bear/10.0
    return bear

while True:
    # gets the value to 1 decimal place in degrees.
    bearing = bearing3599()

    # gets the value as a byte between 0 and 255.
    bear255 = bearing255()

    print bearing
    print bear255
    time.sleep(1)
