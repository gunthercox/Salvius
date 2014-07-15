from marshmallow import Serializer, fields
from robot.joints import Joint


class Ankle(Joint):

    def __init__(self):
        super(Ankle, self).__init__()
        self.angle = 0
        self.tilt = 0

    def set_angle(self, value):
        self.angle = value

    def set_tilt(self, value):
        self.tilt = value


class AnkleSerializer(Serializer):
    angle = fields.Integer()
    tilt = fields.Integer()
