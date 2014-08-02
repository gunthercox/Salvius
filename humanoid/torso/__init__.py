from marshmallow import Serializer, fields
from humanoid.joints import PivotJoint, PivotJointSerializer


class Torso(PivotJoint):

    def __init__(self):
        super(Torso, self).__init__()


class TorsoSerializer(PivotJointSerializer):

    def get_url(self, obj):
        return "/api/robot/body/torso/"
