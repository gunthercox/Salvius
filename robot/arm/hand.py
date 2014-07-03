from marshmallow import Serializer, fields


class Finger(object):

    def __init__(self):
        self.position = 0

    def move(self, degrees):
        """
        Moves a finger a number of degrees relative to the
        current position.
        """
        self.position += degrees

    def relax(self):
        self.position = 0

class Hand(object):

    def __init__(self):
        self.fingers = []

    def add_finger(self, finger):
        self.fingers.append(finger)


class FingerSerializer(Serializer):
    position = fields.Integer()


class HandSerializer(Serializer):
    fingers = fields.Nested(FingerSerializer, many=True)
