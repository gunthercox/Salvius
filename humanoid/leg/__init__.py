from flask.ext.restful import Resource
from flask.ext.restful import marshal, fields, request

from humanoid.leg.hip import Hip
from humanoid.leg.knee import Knee
from humanoid.leg.ankle import Ankle

class Leg(Resource):

    def __init__(self, uuid):
        super(Leg, self).__init__()
        self._hip = Hip(uuid)
        self._knee = Knee(uuid)
        self._ankle = Ankle(uuid)

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
        from flask import current_app as app

        legs = app.config["ROBOT"].db.data(key="legs")    

        # Make sure the leg exists
        if not any(leg["leg"]["id"] == leg_id for leg in legs):
            abort(404, message="Leg id {} does not exist in database".format(leg_id))

        self.data["id"] = leg_id
        self.data["href"] = "/legs/" + str(leg_id) + "/"
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
