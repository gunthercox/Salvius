from humanoid.joints import PivotJoint, PivotJointSerializer


class Torso(PivotJoint):

    def __init__(self):
        super(Torso, self).__init__()
        self.data["href"] = "/api/robot/body/torso/"


class TorsoSerializer(PivotJointSerializer):
    pass
