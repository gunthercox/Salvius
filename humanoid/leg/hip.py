from marshmallow import Serializer, fields
from humanoid.joints import OrthogonalJoint, OrthogonalJointSerializer


class Hip(OrthogonalJoint):

    def __init__(self):
        super(Hip, self).__init__()
        self.parent_id = None

    def set_parent_id(self, uuid):
        self.parent_id = uuid


class HipSerializer(OrthogonalJointSerializer):
    href = fields.Method("get_url")

    def get_url(self, obj):
        return "/api/robot/body/legs/" + str(obj.parent_id) + "/hip/"
