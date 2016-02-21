from flask.views import MethodView
from robotics.decorators import analytics


class Neck(MethodView):
    """
    The tilt of the robot's head is controlled by two
    motors (one on eiter side on the front of the neck).
    """

    @analytics("api_response_time")
    def get(self):
        from flask import abort
        # This method not currently supported.
        abort(405)

    @analytics("api_response_time")
    def patch(self):
        from flask import request, jsonify

        data = request.get_json(force=True)

        if "rotate" in data:
            value = data["rotate"]
            self.rotate(value)

        if "tilt" in data:
            value = data["tilt"]
            self.tilt(value)

        if "lean" in data:
            value = data["lean"]
            self.lean(value)

        return jsonify(data)

    def rotate(self, value):
        """
        Rotate the head clockwise or counter-clockwise.
        """
        from robotics.arduino import Arduino

        neck_controller = Arduino("/dev/ttyACM0")
        neck_controller.write(value)

    def tilt(self, value):
        """
        Angle the head forward or backward.
        """
        pass
        # TODO

    def lean(self, value):
        """
        Angle the head to the left or right.
        """
        pass
        # TODO
