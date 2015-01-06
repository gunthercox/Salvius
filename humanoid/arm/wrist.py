from flask.views import MethodView


class Wrist(MethodView):

    def get(self):
        from flask import abort
        # This method not currently supported.
        abort(405)

    def patch(self, arm_id):
        data = request.get_json(force=True)

        self.validate_fields(data)

        for key in data.keys():
            self.data[key] = data[key]

        return marshal(self.data, self.fields), 201
