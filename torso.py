from flask.views import MethodView
from robotics.decorators import analytics


class Torso(MethodView):

    @analytics("api_response_time")
    def get(self):
        from flask import abort
        # This method not currently supported.
        abort(405)

    @analytics("api_response_time")
    def patch(self):
        from flask import request, jsonify

        data = request.json or {}

        if "rotate" in data:
            value = data["rotate"]
            # TODO

        return jsonify(data)
