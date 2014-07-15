from marshmallow import Serializer, fields
from robot.joints import Joint


class Hip(Joint):

    def __init__(self):
        super(Hip, self).__init__()
        self.angle = 0
        self.position = 0


class HipSerializer(Serializer):
    angle = fields.Integer()
    position = fields.Integer()
