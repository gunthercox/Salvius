from humanoid.robot import Robot
from flask.ext.restful import marshal, fields, request

from humanoid.leg.hip import Hip
from humanoid.leg.knee import Knee
from humanoid.leg.ankle import Ankle

class Leg(Robot):

    def __init__(self):
        super(Leg, self).__init__()
        self._hip = Hip()
        self._knee = Knee()
        self._ankle = Ankle()

        self.data = {}

        self.fields = {
            "id": fields.Integer,
            "href": fields.String,
            "hip": fields.Nested(self._hip.fields),
            "knee": fields.Nested(self._knee.fields),
            "ankle": fields.Nested(self._ankle.fields)
        }

    def get(self, leg_id):
        self.data["id"] = leg_id
        self.data["href"] = "/api/robot/body/legs/" + str(leg_id) + "/"
        self.data["hip"] = dict(self._hip.get(leg_id=leg_id))
        self.data["knee"] = dict(self._knee.get(leg_id=leg_id))
        self.data["ankle"] = dict(self._ankle.get(leg_id=leg_id))

        return marshal(self.data, self.fields)

    def patch(self):
        data = request.get_json(force=True)

        self.validate_fields(data)

        for key in data.keys():
            self.data[key] = data[key]

        return marshal(self.data, self.fields), 201


class Legs(Robot):

    def __init__(self):
        super(Legs, self).__init__()
        self.leg = Leg()

        self.fields = {
            "href": fields.Url("legs", absolute=True),
            "leg": fields.Nested(self.leg.fields)
        }

    def get(self):
        legs = self.db.data(key="legs")

        if not legs:
            return

        leg_list = []

        for leg in legs:
            data = {}
            leg_id = leg["leg"]["id"]
            data["leg"] = dict(self.leg.get(leg_id))
            leg_list.append(data)

        return marshal(leg_list, self.fields)
