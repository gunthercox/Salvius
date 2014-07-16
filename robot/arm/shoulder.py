from marshmallow import Serializer, fields
from robot.joints import Joint


class Shoulder(Joint):

    def __init__(self, rotation=0, angle=0):
        super(Shoulder, self).__init__()
        self.rotation = rotation
        self.angle = angle

    def get_rotation(self):
        return self.rotation

    def get_angle(self):
        return self.angle

    def rotate(self, degrees):
        self.rotation += degrees

    def extend(self, degrees):
        self.angle +=degrees

    def reset(self):
        self.rotation = 0
        self.angle = 0


class ShoulderSerializer(Serializer):
    rotation = fields.Integer()
    angle = fields.Integer()
