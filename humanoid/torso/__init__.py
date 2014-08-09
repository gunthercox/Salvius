from humanoid.joints import PivotJoint


class Torso(PivotJoint):

    def __init__(self):
        super(Torso, self).__init__()
        self.data["href"] = "/api/robot/body/torso/"
