from flask.views import MethodView


class Hip(MethodView):

    def get(self, arm_name):
        from flask import abort
        # This method not currently supported.
        abort(405)

    def patch(self, leg_name):
        from flask import request, jsonify
        data = request.get_json(force=True)

       # TODO

        return jsonify(data)
