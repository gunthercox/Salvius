import time
import zorg


def test():
    #print "x"
    time.sleep(1)

def work(salvius):

    while True:
        #print salvius.camera_one.get_url()
        test()

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
        }
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
    },
    "work": work,
})

api = zorg.api("zorg.api.Http", {})

robot.start()
api.start()
