from marshmallow import Serializer, fields
from humanoid.joints import OrthogonalJoint, OrthogonalJointSerializer


class Shoulder(OrthogonalJoint):

    def __init__(self):
        super(Shoulder, self).__init__()
        self.parent_id = None

        self.data["href"] = "/api/robot/body/arms/" + str(self.parent_id) + "/shoulder/"

    def set_parent_id(self, uuid):
        self.parent_id = uuid
        self.data["href"] = "/api/robot/body/arms/" + str(uuid) + "/shoulder/"


class ShoulderSerializer(OrthogonalJointSerializer):
    pass
