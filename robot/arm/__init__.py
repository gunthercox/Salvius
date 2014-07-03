from marshmallow import Serializer, fields
from shoulder import ShoulderSerializer
from elbow import ElbowSerializer
from wrist import WristSerializer
from hand import HandSerializer


class Arm(object):

    def __init__(self):
        """
        Arm must be designated as 'left' or 'right'.
        """
        self.shoulder = None
        self.elbow = None
        self.wrist = None
        self.hand = None

    def setShoulder(self, shoulder):
        self.shoulder = shoulder

    def setElbow(self, elbow):
        self.elbow = elbow

    def setWrist(self, wrist):
        self.wrist = wrist

    def setHand(self, hand):
        self.hand = hand


class ArmSerializer(Serializer):
    shoulder = fields.Nested(ShoulderSerializer)
    elbow = fields.Nested(ElbowSerializer)
    wrist = fields.Nested(WristSerializer)
    hand = fields.Nested(HandSerializer)

