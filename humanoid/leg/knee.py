from flask.views import MethodView


class Knee(MethodView):
    """
    Knee extends the basic hinge joint class and
    sets a limit to its own movement.
    """

    def get(self, leg_id):
        self.data["href"] = "/legs/" + str(leg_id) + "/knee/"
        # TODO: Check if the arm or leg does not exist in the db.

        return marshal(self.data, self.fields)

    def patch(self, leg_id):
        data = request.get_json(force=True)

        self.validate_fields(data)

        for key in data.keys():
            self.data[key] = data[key]

        return marshal(self.data, self.fields), 201
