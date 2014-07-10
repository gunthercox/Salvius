from marshmallow import Serializer, fields
from robot.head import HeadSerializer
from robot.arm import Arm, ArmSerializer
from robot.leg import LegSerializer


class Body(object):

    def __init__(self):
        self._head = None
        self._arms = []
        self._legs = []

    def set_head(self, head):
        self._head = head

    def new_arm(self):
        """
        Adds an arm object to the body.
        Sets a unique id to reference the listed index of the arm object.
        """
        uuid = 0
        if self._arms:
            uuid = max(arm.id for arm in self._arms) + 1

        arm = Arm(uuid)
        self._arms.append(arm)
        return arm

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
