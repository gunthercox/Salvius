import zorg
import time


def work(salvius):
    from serial import SerialException

    # salvius.neck_servo.set_angle(5)

    '''
    while True:
        salvius.torso_left_hbridge.turn_off()
        time.sleep(1)
        salvius.torso_left_hbridge.rotate_clockwise()
        time.sleep(1)
        salvius.torso_left_hbridge.rotate_counterclockwise()
        time.sleep(1)
        salvius.torso_left_hbridge.turn_off()

    return True
    '''

    using_emic = True

    try:
        salvius.speech_synthesis.start()
        salvius.speech_synthesis.set_voice(1)
    except SerialException:
        using_emic = False

    salvius.speech_recognition.start()

    while True:
        try:
            recognized_speech = salvius.speech_recognition.get_words()

            if recognized_speech:

                print(recognized_speech)

                if using_emic:
                    response = salvius.communication.get_response(
                        recognized_speech
                    )
                    salvius.speech_synthesis.speak(response)
                else:
                    salvius.speech_recognition.stop()
                    salvius.speech_synthesis2.reply(recognized_speech)
                    salvius.speech_recognition.start()

            time.sleep(1)
        except (KeyboardInterrupt, EOFError, SystemExit):
            break


def main():
    robot = zorg.robot({
        "name": "Salvius",
        "connections": {
            "camera": {
                "adaptor": "zorg_network_camera.Camera",
                "url": "http://192.168.1.6/image.jpg"
            },
            "arduino_leonardo": {
                "adaptor": "zorg_firmata.Firmata",
                "port": "/dev/ttyACM0"
            },
            "chatterbot": {
                "adaptor": "salvius.communication.Conversation",
                "io_adapter": "chatterbot.adapters.io.JsonAdapter"
            },
            "serial": {
                "adaptor": "zorg_emic.Serial",
                "port": "/dev/ttyAMA0"
            },
            "sphinx": {
                "adaptor": "salvius.speech.SpeechRecognition",
                "recognizer_function": "recognize_sphinx"
            },
            "analytics": {
                "adaptor": "iot_analytics.apps.zorg.GoogleAnalytics",
                "property_id": "UA-12573345-12",
                "client_id": "salvius"
            },
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
            "neck_servo": {
                "connection": "arduino_leonardo",
                "driver": "zorg_grove.Servo",
                "pin": 6
            },
            "torso_right_hbridge": {
                "connection": "arduino_leonardo",
                "driver": "hbridge.ServoHBridge",
                "pin": 5
            },
            "torso_left_hbridge": {
                "connection": "arduino_leonardo",
                "driver": "hbridge.RelayHBridge",
                "pins": [4, 5, 6, 7]
            },
            "communication": {
                "connection": "chatterbot",
                "driver": "salvius.communication.ApiDriver"
            },
            "speech_synthesis": {
                "connection": "serial",
                "driver": "zorg_emic.Emic2"
            },
            "speech_synthesis2": {
                "connection": "chatterbot",
                "driver": "salvius.speech.SpeechSynthesis"
            },
            "speech_recognition": {
                "connection": "sphinx",
                "driver": "salvius.speech.ApiDriver"
            },
            "touch_sensor": {
                "connection": "analytics",
                "driver": "iot_analytics.apps.zorg.drivers.Event"
            }
        },
        "work": work,
    })

    api = zorg.api("zorg.api.Http", {})

    try:
        robot.start()
        api.start()
    except (KeyboardInterrupt, EOFError, SystemExit):
        pass


if __name__ == "__main__":
    main()
