from marshmallow import Serializer, fields

class Ankle(object):

    def __init__(self):
        self.angle = 0
        self.tilt = 0


class AnkleSerializer(Serializer):
    angle = fields.Integer()
    tilt = fields.Integer()
