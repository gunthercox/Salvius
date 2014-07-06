from marshmallow import Serializer, fields
from .body import Body, BodySerializer


class Robot(object):

    def __init__(self, name=""):
        self._body = Body()
        self.name = name

    @property
    def body(self):
        return self._body


class RobotSerializer(Serializer):
    name = fields.String()
    body = fields.Nested(BodySerializer)
