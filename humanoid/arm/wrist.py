from marshmallow import Serializer, fields
from humanoid.joints import ArticulatedJoint, ArticulatedJointSerializer


class Wrist(ArticulatedJoint):

    def __init__(self):
        super(Wrist, self).__init__()
        self.parent_id = None

        self.data["href"] = "/api/robot/body/arms/" + str(self.parent_id) + "/wrist/"

    def set_parent_id(self, uuid):
        self.parent_id = uuid
        self.data["href"] = "/api/robot/body/arms/" + str(self.parent_id) + "/wrist/"


class WristSerializer(ArticulatedJointSerializer):
    pass
