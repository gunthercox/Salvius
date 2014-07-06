from marshmallow import Serializer, fields

class Foot(object):

    def __init__(self):
        self.toes = []

    def self.add_toes(self, toe):
        self.toes.append(toe)
