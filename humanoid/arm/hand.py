from flask.views import MethodView


class Finger(MethodView):

    def get(self):
        from flask import abort
        # This method not currently supported.
        abort(405)

    def patch(self, arm_id, finger_id):
        data = request.get_json(force=True)

        self.validate_fields(data)

        for key in data.keys():
            self.data[key] = data[key]

        return marshal(self.data, self.fields), 201


class Thumb(MethodView):
    """
    Thumbs work very similar to fingers, however they have other attributes
    which allow them to be opposable.
    """

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
