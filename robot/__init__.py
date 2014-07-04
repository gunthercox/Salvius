from marshmallow import Serializer, fields
from .body import BodySerializer

class Robot(object):

    def __init__(self, name=""):
        self.name = name
        self.body = None

    def set_body(self, body):
        self.body = body

class RobotSerializer(Serializer):
    name = fields.String()
    body = fields.Nested(BodySerializer)
