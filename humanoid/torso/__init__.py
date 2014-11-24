from humanoid.joints import PivotJoint


class Torso(PivotJoint):

    def __init__(self):
        super(Torso, self).__init__()
        self.data["href"] = "/torso/"
