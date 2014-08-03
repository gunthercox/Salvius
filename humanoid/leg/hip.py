from marshmallow import Serializer, fields
from humanoid.joints import OrthogonalJoint, OrthogonalJointSerializer


class Hip(OrthogonalJoint):

    def __init__(self):
        super(Hip, self).__init__()
        self.parent_id = None

        self.data["href"] = "/api/robot/body/legs/" + str(self.parent_id) + "/hip/"

    def set_parent_id(self, uuid):
        self.parent_id = uuid
        self.data["href"] = "/api/robot/body/legs/" + str(uuid) + "/hip/"


class HipSerializer(OrthogonalJointSerializer):
    pass
