from marshmallow import Serializer, fields

class Torso(object):

    def __init__(self):
        self.rotation = 0

    def move(self, roataion):
        self.rotation += roataion


class TorsoSerializer(Serializer):
    rotation = fields.Integer()
