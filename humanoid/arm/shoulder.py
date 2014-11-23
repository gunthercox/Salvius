from flask.ext.restful import marshal, request
from humanoid.joints import OrthogonalJoint, OrthogonalJointSerializer


class Shoulder(OrthogonalJoint):

    def __init__(self):
        super(Shoulder, self).__init__()
        self.parent_id = None

        self.data["href"] = "/arms/" + str(self.parent_id) + "/shoulder/"

    def set_parent_id(self, uuid):
        self.parent_id = uuid
        self.data["href"] = "/arms/" + str(uuid) + "/shoulder/"

    def get(self, arm_id):
        self.set_parent_id(arm_id)
        return marshal(self.data, self.fields)

    def patch(self, arm_id):
        data = request.get_json(force=True)

        self.validate_fields(data)

        for key in data.keys():
            self.data[key] = data[key]

        return marshal(self.data, self.fields), 201


class ShoulderSerializer(OrthogonalJointSerializer):
    pass
