from marshmallow import Serializer, fields
from ..head import HeadSerializer
from ..arm import ArmSerializer
from ..leg import LegSerializer


class Body(object):

    def __init__(self):
        self._head = None
        self._arms = []
        self._legs = []

    def set_head(self, head):
        self._head = head

    def add_arm(self, arm):
        self._arms.append(arm)

    def add_leg(self, leg):
        self.legs.append(leg)

    @property
    def head(self):
        return self._head

    @property
    def arms(self):
        return self._arms

    @property
    def legs(self):
        return self._legs


class BodySerializer(Serializer):
    head = fields.Nested(HeadSerializer)
    arms = fields.Nested(ArmSerializer, many=True)
    legs = fields.Nested(LegSerializer, many=True)
