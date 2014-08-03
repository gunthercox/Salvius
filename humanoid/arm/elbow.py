from marshmallow import fields
from humanoid.joints import HingeJoint, HingeJointSerializer


class Elbow(HingeJoint):
    """
    Elbow extends the basic hinge joint class and
    sets a limit to its own movement.
    """

    def __init__(self):
        super(Elbow, self).__init__()

        # Number of degrees that the joint is limited to.
        self.limit = 180

        self.parent_id = None

        self.data["href"] = "/api/robot/body/arms/" + str(self.parent_id) + "/elbow/"

    def set_parent_id(self, uuid):
        self.parent_id = uuid
        self.data["href"] = "/api/robot/body/arms/" + str(uuid) + "/elbow/"


class ElbowSerializer(HingeJointSerializer):
    limit = fields.Integer()
