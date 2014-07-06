from marshmallow import Serializer, fields

class Toes(object):

    def __init__(self):
        self.position = 0

    def set_position(self, position):
        self.position = position


class Foot(object):

    def __init__(self):
        self.toes = []

    def add_toes(self, toe):
        self.toes.append(toe)


class FootSerializer(Serializer):
    position = fields.Integer()


class FootSerializer(Serializer):
    toes = fields.Nested(FootSerializer, many=True)
