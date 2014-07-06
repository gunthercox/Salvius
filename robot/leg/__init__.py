from marshmallow import Serializer, fields
from .hip import Hip, HipSerializer
from .knee import Knee, KneeSerializer
from .ankle import Ankle, AnkleSerializer
from .foot import Foot, FootSerializer


class Leg(object):

    def __init__(self):
        self.hip = None
        self.knee = None
        self.ankle = None
        self.foot = None

    def set_hip(self, hip):
        self.hip = hip

    def set_knee(self, knee):
        self.knee = knee

    def set_ankle(self, ankle):
        self.ankle = ankle

    def set_foot(self, foot):
        self.foot = foot

    def get_hip(self):
        return self.hip

    def get_knee(self):
        return self.knee

    def get_ankle(self):
        return self.ankle

    def get_foot(self):
        return self.foot


class LegSerializer(Serializer):
    hip = fields.Nested(HipSerializer)
    knee = fields.Nested(KneeSerializer)
    ankle = fields.Nested(AnkleSerializer)
    foot = fields.Nested(FootSerializer)

