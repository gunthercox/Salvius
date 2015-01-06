from flask.views import MethodView


class Ankle(MethodView):

    def get(self, leg_id):
        self.data["href"] = "/legs/" + str(leg_id) + "/ankle/"

        return marshal(self.data, self.fields)

    def patch(self, leg_id):
        data = request.get_json(force=True)

        self.validate_fields(data)

        for key in data.keys():
            self.data[key] = data[key]

        return marshal(self.data, self.fields), 201
