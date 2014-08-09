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
        from flask.ext.restful import abort

        legs = self.db.data(key="legs")    

        # Make sure the leg exists
        if not any(leg["leg"]["id"] == leg_id for leg in legs):
            abort(404, message="Leg id {} does not exist in database".format(leg_id))

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
            "legs": fields.List(fields.Nested(self.leg.fields))
        }

    def get(self):
        legs = self.db.data(key="legs")

        leg_list = []

        for leg in legs:
            leg_id = leg["leg"]["id"]
            leg_list.append(dict(self.leg.get(leg_id)))

        data = {}
        data["legs"] = leg_list

        return marshal(data, self.fields)
