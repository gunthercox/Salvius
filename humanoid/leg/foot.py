from marshmallow import Serializer, fields


'''
# Toes are commented out because they are not a part of the Salvius humanoid model.
# Please submit a support ticket if interest in this feature exists.
class Toes(object):

    def __init__(self):
        self.position = 0

    def set_position(self, position):
        self.position = position
'''

class Foot(object):

    def __init__(self):
        #self.toes = []
        self.sensors = []

    #def add_toes(self, toe):
        #self.toes.append(toe)


class FootSerializer(Serializer):
    #toes = fields.Nested(FootSerializer, many=True)
    sensors = fields.List(fields.Integer)
