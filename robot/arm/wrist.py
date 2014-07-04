from marshmallow import Serializer, fields


class Wrist(object):

    def __init__(self):
        self.roll = 0
        self.pitch = 0
        self.yaw = 0

    def rotate(self, degrees):
        """
        Takes a positive or negative number to rotate the wrist
        relative to its current position.
        """
        self.roll += degrees

    def tilt(self, degrees):
        """
        Tilts writs
        """
        self.pitch += degrees

    def lean(self, degrees):
        """
        Angles the wrist left or right.
        """
        self.yaw += degrees

    def reset(self):
        self.roll = 0
        self.pitch = 0
        self.yaw = 0

    def get_position(self):
        return [self.roll, self.pitch, self.yaw]


class WristSerializer(Serializer):
    roll = fields.Integer()
    pitch = fields.Integer()
    yaw = fields.Integer()
