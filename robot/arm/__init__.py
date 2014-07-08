from marshmallow import Serializer, fields
from .shoulder import ShoulderSerializer
from .elbow import ElbowSerializer
from .wrist import WristSerializer
from .hand import HandSerializer


class Arm(object):

    def __init__(self):
        self._shoulder = None
        self._elbow = None
        self._wrist = None
        self._hand = None

    def set_shoulder(self, shoulder):
        self._shoulder = shoulder

    def set_elbow(self, elbow):
        self._elbow = elbow

    def set_wrist(self, wrist):
        self._wrist = wrist

    def set_hand(self, hand):
        self._hand = hand

    @property
    def shoulder(self):
        return self._shoulder

    @property
    def elbow(self):
        return self._elbow

    @property
    def wrist(self):
        return self._wrist

    @property
    def hand(self):
        return self._hand


class ArmSerializer(Serializer):
    shoulder = fields.Nested(ShoulderSerializer)
    elbow = fields.Nested(ElbowSerializer)
    wrist = fields.Nested(WristSerializer)
    hand = fields.Nested(HandSerializer)

