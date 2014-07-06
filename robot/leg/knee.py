from marshmallow import Serializer, fields

class Knee(object):

    def __init__(self):
        self.angle = 0


class KneeSerializer(Serializer):
    angle = fields.Integer()
