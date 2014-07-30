from marshmallow import Serializer, fields
from robot.joints import OrthogonalJoint, OrthogonalJointSerializer


class Shoulder(OrthogonalJoint):

    def __init__(self, rotation=0, angle=0):
        super(Shoulder, self).__init__()
        self.parent_id = None

    def set_parent_id(self, uuid):
        self.parent_id = uuid


class ShoulderSerializer(OrthogonalJointSerializer):
    href = fields.Method("get_url")

    def get_url(self, obj):
        return "/api/robot/body/arms/" + str(obj.parent_id) + "/shoulder/"
