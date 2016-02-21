from flask.views import MethodView


class Ankle(MethodView):

    def get(self, arm_name):
        from flask import abort
        # This method not currently supported.
        abort(405)

    def patch(self, leg_name):
        from flask import request
        data = request.get_json(force=True)

        # TODO

        return [self.data, self.fields, 201]
