from marshmallow import Serializer, fields


class Elbow(object):

    def __init__(self, angle=0):
        self.angle = angle

    def move(self, degrees):
        """
        Moves the elbow relative to its current position.
        """
        self.angle += degrees

    def relax(self):
        self.angle = 0

class ElbowSerializer(Serializer):
    angle = fields.Integer()
