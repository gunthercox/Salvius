from marshmallow import Serializer, fields
from .shoulder import ShoulderSerializer
from .elbow import ElbowSerializer
from .wrist import WristSerializer
from .hand import HandSerializer


class Arm(object):

    def __init__(self):
        self.shoulder = None
        self.elbow = None
        self.wrist = None
        self.hand = None

    def set_shoulder(self, shoulder):
        self.shoulder = shoulder

    def set_elbow(self, elbow):
        self.elbow = elbow

    def set_wrist(self, wrist):
        self.wrist = wrist

    def set_hand(self, hand):
        self.hand = hand

    def get_shoulder(self):
        return self.shoulder

    def get_elbow(self):
        return self.elbow

    def get_wrist(self):
        return self.wrist

    def get_hand(self):
        return self.hand


class ArmSerializer(Serializer):
    shoulder = fields.Nested(ShoulderSerializer)
    elbow = fields.Nested(ElbowSerializer)
    wrist = fields.Nested(WristSerializer)
    hand = fields.Nested(HandSerializer)

