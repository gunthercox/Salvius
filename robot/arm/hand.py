from marshmallow import Serializer, fields


class Finger(object):

    def __init__(self, uuid):
        self.position = 0
        self.id = uuid

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

    def unid(self, unid):
        self.id = unid

class Hand(object):

    def __init__(self):
        self._fingers = []
        self._thumb = None

    def add_finger(self):
        """
        Adds a finger to the hand
        """
        maxx = 0
        for finger in self._fingers:
            if finger.id > maxx:
                maxx = finger.id

        maxx += 1

        # Future: handle the above loop better
        #un = max(self._fingers.y for id in self.id)

        finger = Finger(maxx)

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
    href = fields.Method("get_url")
    id = fields.Integer()
    position = fields.Integer()

    def get_url(self, obj):

        # temp placeholder
        arm_id = 0

        url = "/api/robot/body/arms/" + str(arm_id) + "/hand"
        if self.many:
            url += "/fingers/" + str(obj.id)
        else:
            url += "/thumb"

        return url


class HandSerializer(Serializer):
    fingers = fields.Nested(FingerSerializer, many=True)
    thumb = fields.Nested(FingerSerializer)

