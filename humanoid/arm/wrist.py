from marshmallow import Serializer, fields
from humanoid.joints import ArticulatedJoint, ArticulatedJointSerializer


class Wrist(ArticulatedJoint):

    def __init__(self):
        super(Wrist, self).__init__()
        self.parent_id = None

    def set_parent_id(self, uuid):
        self.parent_id = uuid


class WristSerializer(ArticulatedJointSerializer):
    href = fields.Method("get_url")

    def get_url(self, obj):
        return "/api/robot/body/arms/" + str(obj.parent_id) + "/wrist/"
