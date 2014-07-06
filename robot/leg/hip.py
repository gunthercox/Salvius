from marshmallow import Serializer, fields

class Hip(object):

    def __init__(self):
        self.angle = 0
        self.position = 0

class HipSerializer(Serializer):
    angle = fields.Integer()
    position = fields.Integer()
