from marshmallow import Serializer, fields
from humanoid.neck import Neck, NeckSerializer
from humanoid.torso import Torso, TorsoSerializer
from humanoid.arm import Arm, ArmSerializer
from humanoid.leg import Legs


class Body(object):

    def __init__(self):
        self.neck = Neck()
        self.torso = Torso()
        self._arms = []
        self._legs = Legs()

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

    @property
    def arms(self):
        return self._arms

    @property
    def legs(self):
        return self._legs.get()


class BodySerializer(Serializer):
    neck = fields.Nested(NeckSerializer)
    torso = fields.Nested(TorsoSerializer)
    arms = fields.Nested(ArmSerializer, many=True)
    legs = fields.String()


class ArmsSerializer(Serializer):
    arms = fields.Nested(ArmSerializer, many=True)
