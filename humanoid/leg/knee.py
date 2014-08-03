from marshmallow import fields
from humanoid.joints import HingeJoint, HingeJointSerializer


class Knee(HingeJoint):
    """
    Knee extends the basic hinge joint class and
    sets a limit to its own movement.
    """

    def __init__(self):
        super(Knee, self).__init__()

        # Number of degrees that the joint is limited to.
        self.limit = 180

        self.parent_id = None

        self.data["href"] = "/api/robot/body/legs/" + str(self.parent_id) + "/knee/"

    def set_parent_id(self, uuid):
        self.parent_id = uuid
        self.data["href"] = "/api/robot/body/legs/" + str(uuid) + "/knee/"


class KneeSerializer(HingeJointSerializer):
    limit = fields.Integer()
