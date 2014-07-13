from marshmallow import fields
from robot.joints import HingeJoint, HingeJointSerializer


class Elbow(HingeJoint):
    """
    Elbow extends the basic hinge joint class and
    sets a limit to its own movement.
    """

    def __init__(self):
        super(Elbow, self).__init__()

        # Number of degrees that the joint is limited to.        
        self.limit = 180


class ElbowSerializer(HingeJointSerializer):
    limit = fields.Integer()
