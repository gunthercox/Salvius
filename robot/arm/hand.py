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

    def reset(self):
        self.position = 0

    def get_position(self):
        return self.position

class Hand(object):

    def __init__(self):
        self._fingers = []
        self._thumb = None

    def add_finger(self, finger):
        self._fingers.append(finger)

    def set_thumb(self, thumb):
        """
        Takes a finger object as a parameter.
        """
        self._thumb = thumb

    @property
    def fingers(self):
        return self._fingers

    @property
    def thumb(self):
        return self._thumb

    def close(self):
        """
        Closes all of the hands fingers to make a fist shape.
        """
        for finger in self._fingers:
            finger.move(100)
        self._thumb.move(100)


class FingerSerializer(Serializer):
    position = fields.Integer()


class HandSerializer(Serializer):
    fingers = fields.Nested(FingerSerializer, many=True)
    thumb = fields.Nested(FingerSerializer)

