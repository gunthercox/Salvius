from marshmallow import Serializer, fields
from humanoid.joints import ArticulatedJoint, ArticulatedJointSerializer


class Neck(ArticulatedJoint):
    """
    The tilt of the robot's head is controlled by two
    motors (one on eiter side on the front of the neck).
    """

    def __init__(self):
        super(Neck, self).__init__()


class NeckSerializer(ArticulatedJointSerializer):

    def get_url(self, obj):
        return "/api/robot/body/neck/"
