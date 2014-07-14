from marshmallow import Serializer, fields
from robot.leg.hip import Hip, HipSerializer
from robot.leg.knee import Knee, KneeSerializer
from robot.leg.ankle import Ankle, AnkleSerializer
from robot.leg.foot import Foot, FootSerializer


class Leg(object):

    def __init__(self, uuid):
        self._hip = None
        self._knee = None
        self._ankle = None
        self._foot = None

        self.id = uuid

    def set_hip(self, hip):
        self._hip = hip

    def set_knee(self, knee):
        self._knee = knee

    def set_ankle(self, ankle):
        self._ankle = ankle

    def set_foot(self, foot):
        self._foot = foot

    @property
    def hip(self):
        return self._hip

    @property
    def knee(self):
        return self._knee

    @property
    def ankle(self):
        return self._ankle

    @property
    def foot(self):
        return self._foot


class LegSerializer(Serializer):
    id = fields.UUID()
    href = fields.Method("get_url")
    hip = fields.Nested(HipSerializer)
    knee = fields.Nested(KneeSerializer)
    ankle = fields.Nested(AnkleSerializer)
    foot = fields.Nested(FootSerializer)

    def get_url(self, obj):
        return "/api/robot/body/legs/" + str(obj.id)

