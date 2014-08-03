from flask.ext.restful import marshal, request

from humanoid.joints import ArticulatedJoint, ArticulatedJointSerializer


class Ankle(ArticulatedJoint):

    def __init__(self):
        super(Ankle, self).__init__()
        self.parent_id = None

        self.data["href"] = "/api/robot/body/legs/" + str(self.parent_id) + "/ankle/"

    def set_parent_id(self, uuid):
        self.parent_id = uuid
        self.data["href"] = "/api/robot/body/legs/" + str(uuid) + "/ankle/"

    def get(self, leg_id):
        self.data["href"] = "/api/robot/body/legs/" + str(leg_id) + "/ankle/"
        # TODO: Create arm and leg representation in database,
        # An error will be thrown if the arm or leg does not exist in the db.

        return marshal(self.data, self.fields)

    def patch(self, leg_id):
        data = request.get_json(force=True)

        self.validate_fields(data)

        for key in data.keys():
            self.data[key] = data[key]

        return marshal(self.data, self.fields), 201


class AnkleSerializer(ArticulatedJointSerializer):
    pass
