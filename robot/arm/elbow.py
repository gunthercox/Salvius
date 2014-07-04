from marshmallow import Serializer, fields


class Elbow(object):

    def __init__(self, angle=0):
        self.angle = angle

    def move(self, degrees):
        """
        Moves the elbow relative to its current position.
        """
        self.angle += degrees

    def reset(self):
        self.angle = 0

    def get_angle(self):
        return self.angle

class ElbowSerializer(Serializer):
    angle = fields.Integer()
