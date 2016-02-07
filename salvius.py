import time
import zorg


def work(salvius):

    salvius.speech_synthesis.start()
    salvius.speech_synthesis.set_voice(1)

    salvius.speech_recognition.start()

    while True:
        try:
            recognized_speech = salvius.speech_recognition.get_words()
            if recognized_speech:
                print(recognized_speech)
            time.sleep(1)
        except (KeyboardInterrupt, EOFError, SystemExit):
            break

robot = zorg.robot({
    "name": "Salvius",
    "connections": {
        "camera": {
            "adaptor": "zorg_network_camera.Camera",
            "url": "http://192.168.1.6/image.jpg"
        },
        "chatterbot": {
            "adaptor": "communication.Conversation",
            "io_adapter": "chatterbot.adapters.io.JsonAdapter"
        },
        "serial": {
            "adaptor": "zorg_emic.Serial",
            "port": "/dev/ttyAMA0",
        },
        "speech_recognition": {
            "adaptor": "speech.SpeechRecognition",
            "recognizer_function": "recognize_sphinx"
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
        "speech_synthesis": {
            "connection": "serial",
            "driver": "zorg_emic.Emic2",
        },
        "speech_recognition": {
            "connection": "speech_recognition",
            "driver": "speech.ApiDriver",
        },
        "touch_sensor": {
            "connection": "analytics",
            "driver": "iot_analytics.apps.zorg.drivers.Event",
        }
    },
    "work": work,
})

api = zorg.api("zorg.api.Http", {})

if __name__ == "__main__":
    try:
        robot.start()
        api.start()
    except (KeyboardInterrupt, EOFError, SystemExit):
        pass
