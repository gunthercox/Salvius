from flask.views import MethodView


class Finger(MethodView):

    def get(self, arm_name):
        from flask import abort
        # This method not currently supported.
        abort(405)

    def patch(self, arm_name):
        from flask import request, jsonify

        data = request.get_json(force=True)

        # TODO

        return jsonify(data)


class Thumb(MethodView):
    """
    Thumbs work very similar to fingers, however they have other attributes
    which allow them to be opposable.
    """

    def get(self, arm_name):
        from flask import abort
        # This method not currently supported.
        abort(405)

    def patch(self, arm_name):
        from flask import request, jsonify

        data = request.get_json(force=True)

        # TODO

        return jsonify(data)
