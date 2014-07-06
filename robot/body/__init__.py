from marshmallow import Serializer, fields
from ..head import HeadSerializer
from ..arm import ArmSerializer
from ..leg import LegSerializer


class Body(object):

    def __init__(self):
        self.head = None
        self._arms = []
        self.legs = []

    def add_head(self, head):
        self.head.append(head)

    def add_arm(self, arm):
        self._arms.append(arm)

    def add_legs(self, leg):
        self.legs.append(leg)

    @property
    def arms(self):
        return self._arms


class BodySerializer(Serializer):
    head = fields.Nested(HeadSerializer)
    arms = fields.Nested(ArmSerializer, many=True)
    legs = fields.Nested(LegSerializer, many=True)
