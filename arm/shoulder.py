from flask.views import MethodView


class Shoulder(MethodView):

    def get(self, arm_name):
        from flask import abort
        # This method not currently supported.
        abort(405)

    def patch(self, arm_name):
        from flask import request, jsonify

        data = request.json or {}

        if "rotate" in data:
            value = data["rotate"]
            # TODO

        if "extend" in data:
            value = data["extend"]
            # TODO

        return jsonify(data)
