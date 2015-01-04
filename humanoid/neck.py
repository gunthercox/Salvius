from flask.views import MethodView


class Neck(MethodView):
    """
    The tilt of the robot's head is controlled by two
    motors (one on eiter side on the front of the neck).
    """

    def get(self):
        from flask import abort
        # This method not currently supported.
        abort(405)

    def patch(self):
        from flask import request, jsonify

        data = request.json or {}

        if "rotate" in data:
            value = data["rotate"]
            # TODO

        return jsonify(data)

    def rotate(self, value):
        """
        Rotate the head clockwise or counter-clockwise.
        """

    def tilt(self, value):
        """
        Angle the head forward or backward.
        """
        pass

    def lean(self, value):
        """
        Angle the head to the left or right.
        """
        pass
        
