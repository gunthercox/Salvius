from marshmallow import Serializer, fields
from humanoid.leg.hip import Hip, HipSerializer
from humanoid.leg.knee import Knee, KneeSerializer
from humanoid.leg.ankle import Ankle, AnkleSerializer


class Leg(object):

    def __init__(self, uuid):
        self._hip = None
        self._knee = None
        self._ankle = None

        self.id = uuid

    def set_hip(self, hip):
        self._hip = hip

    def set_knee(self, knee):
        self._knee = knee

    def set_ankle(self, ankle):
        self._ankle = ankle

    @property
    def hip(self):
        return self._hip

    @property
    def knee(self):
        return self._knee

    @property
    def ankle(self):
        return self._ankle


class LegSerializer(Serializer):
    id = fields.UUID()
    hip = fields.Nested(HipSerializer)
    knee = fields.Nested(KneeSerializer)
    ankle = fields.Nested(AnkleSerializer)

    def get_url(self, obj):
        return "/api/robot/body/legs/" + str(obj.id)
