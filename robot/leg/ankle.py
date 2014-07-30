from marshmallow import Serializer, fields
from robot.joints import ArticulatedJoint, ArticulatedJointSerializer


class Ankle(ArticulatedJoint):

    def __init__(self):
        super(Ankle, self).__init__()
        self.parent_id = None

    def set_parent_id(self, uuid):
        self.parent_id = uuid


class AnkleSerializer(ArticulatedJointSerializer):
    href = fields.Method("get_url")

    def get_url(self, obj):
        return "/api/robot/body/legs/" + str(obj.parent_id) + "/ankle/"
