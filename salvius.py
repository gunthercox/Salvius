import time
import zorg


def work(salvius):

    robot.touch_sensor.send(
        category='server',
        action='started'
    )

    while True:
        time.sleep(1)

robot = zorg.robot({
    "name": "Salvius",
    "connections": {
        "camera": {
            "adaptor": "zorg_network_camera.Camera",
            "url": "http://192.168.1.6/image.jpg"
        },
        "chatterbot": {
            "adaptor": "communication.Conversation"
        },
        "serial": {
            "adaptor": "zorg_emic.Serial",
            "port": "/dev/ttyAMA0",
        },
        "analytics": {
            "adaptor": "iot_analytics.apps.zorg.GoogleAnalytics",
            "property_id": "UA-12573345-12",
            "client_id": "salvius",
        },
        #"raspberry_pi": {
            # "adaptor": "zorg-raspi.RasPi",
        #},
    },
    "devices": {
        "camera_one": {
            "connection": "camera",
            "driver": "zorg_network_camera.Feed"
        },
        "camera_ocr": {
            "connection": "camera",
            "driver": "zorg_network_camera.OCR"
        },
        "communication": {
            "connection": "chatterbot",
            "driver": "communication.ApiDriver"
        },
        "speech": {
            "connection": "serial",
            "driver": "zorg_emic.Emic2",
        },
        "touch_sensor": {
            "connection": "analytics",
            "driver": "iot_analytics.apps.zorg.drivers.Event",
        }
    },
    "work": work,
})

api = zorg.api("zorg.api.Http", {})

robot.start()
api.start()
