from flask.views import MethodView


class Knee(MethodView):
    """
    Knee extends the basic hinge joint class and
    sets a limit to its own movement.
    """

    def get(self, leg_name):
        from flask import abort
        # This method not currently supported.
        abort(405)

    def patch(self, leg_name):
        from flask import request, jsonify
        data = request.get_json(force=True)

        # TODO

        return jsonify(data)
