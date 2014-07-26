#Salvius [![Build Status](https://travis-ci.org/gunthercox/salvius.svg?branch=master)](https://travis-ci.org/gunthercox/salvius)

![Project photos](http://i.imgur.com/4sXpuA4.png)

This repository contains the source code for Salvius, a robot who uses a 
Rapsberry Pi and several Arduino microcontrollers as a brain.

> Salvius is a robot made out of recycled materials
> and designed to be able to perform a wide range of
> tasks by having a body structure that is similar to
> that of a human. The primary goal for Salvius is to 
> create a humanoid robot that will be able to function
> dynamically in a domestic environment.
> ~ [salviusrobot.blogspot.com](http://salviusrobot.blogspot.com)

**Key features:**
  - Web based user interface
  - Easily customizable robots
  - RESTfull API
  - Modular design makes it easy to add controllers via I2C

## Setup
Installing this software on your robot should be easy. Once you have downloaded 
the latest copy into a directory on your Rapsberry Pi, you can download and 
configure the robot's api and interface by running the following three lines of code.

```bash
apt-get install pip
pip install -r requirements.md
chmod a+x robot.py
```

To enable I2C communication on the Rapsberry Pi, edit
```/etc/modprobe.d/raspi-blacklist.conf``` and make sure that the line ```blacklist i2c-bcm2708``` is commented out. Also edit ```/etc/modules``` and make sure that the line ```i2c-dev``` exists somewhere in the file.
Be sure to **apt-get install** i2c-tools and python-smbus.
To configure the software, we will add the Pi user to the I2C access group, by running the command sudo adduser pi i2c.
Reboot after installing the required packages.

To test the configuration, run the command ```i2cdetect -y 0``` to display anything connected. A typical response showing that nothing is connected should look like this:

```
0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f
00:          -- -- -- -- -- -- -- -- -- -- -- -- --
10: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
20: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
30: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
40: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
50: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
60: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
70: -- -- -- -- -- -- -- --
```

Use the following to run the robot's server.
```bash
python robot.py runserver
```

## Features

### Text to speech
The robot uses a speech synthesis library to convert processed text into verbal sounds.
Checkout the repo for this library here: https://github.com/jscrane/TTS

### Speech recognition
This is still a bit of a work in progress, at best a few small words can be recognised.

### Handwriting

The robot can hold a pen and write when given a string of text.
The robot's handwriting is based on a grid in which each letter is created as a
result of horizontal and vertical lines.

### Communication experiment
I've included a package which allows the robot to tweet randomly selected 
messages to Twitter accounts. For now the robot cannot reply to users, however 
I have plans to add this feature. To use this feature you will need to register 
your app on https://dev.twitter.com/apps to get the token and secret keys. 
You will then need to create a file ```settings.py``` in the ```twitter``` 
directory with the following dictionary pointing to your Twitter keys and tokens.

```python
# Set DEBUG flag to true for testing
DEBUG = True

# Twitter api
TWITTER = {
    'CONSUMER_KEY': '',
    'CONSUMER_SECRET': '',
    'TOKEN': '',
    'TOKEN_SECRET': ''
}
```

## Modular robot library
The robot library included in this project can be used to easially build and
customize robots. The library is **ideal for humanoid** type robots, however it
could also work well with quadropeds and other types of robots.

To build a custom robot you must first create a new robot object. The robot
object is a container for each of the submodules required to build a robot.

```
from robot import Robot
robot = new Robot("Robot Name")
```

The robot object provides assess to skill modules that handle capabiliteis such
as speech, but also component modules which allow physical parts of the robot
to be assembled.

Environmental effectors such as arms and legs can be added to a the robot's body
object.

```python
arm = Arm()
body.add_arm(arm)
```

Various robots can be constructed following a basic humanod disign. A modified
robot could, for instance, have only three fingers.

```python
fingers = [Finger(), Finger(), Finger(), Finger()]
for finger in fingers:
    hand.add_finger(finger)
```

Once the physical robot has been constructed, the robot library provides access
to usefull methods to allow you to control its movements.

The robot object is also serialized to privide a web based endpoint to post data
to inorder to control the robot. The endpoint's structure reflects how each of
the robot's components contain their sub-components.

A robot with one arm would look like this:

```json
{
  "body": {
    "arms": [
      {
        "elbow": {
          "angle": 0
        },
        "hand": {
          "fingers": [
            {
              "position": 0
            },
            {
              "position": 0
            },
            {
              "position": 0
            },
            {
              "position": 0
            }
          ],
          "thumb": {
            "position": 0
          }
        },
        "shoulder": {
          "angle": 0,
          "rotation": 0
        },
        "wrist": {
          "pitch": 0,
          "roll": 0,
          "yaw": 0
        }
      }
    ]
  },
  "name": "Robot Name"
}
```

A specific part of the robot can be accessed by changing the url to narrow the
objects that are serialized.

The url ```/api/robot/body/arms/0/hand/fingers/0/``` would return
only the serialized representation of the first finger on the first arm attached
to the robot. This data would be shown as follows, showing only the numeric
position of that one finger.

```json
{
  "position": 0
}
```

## Tests
The code for this project is automatically tested to ensure that class methods
perform as expected. These tests can also be run manually by running the command
```nosetests``` from within the repository's root directory. See 
([unit tests](http://en.wikipedia.org/wiki/Unit_testing)) for more information.

## Notes

**SSH into Rapsberry Pi:** ```ssh pi@192.168.1.4``` (Your local ip may differ)
The default password is ```password```

## Contributors
This project has been made possible with funding from the following sources:
Jennifer Cox, Adam Iredale, Janet Wise, Glen Zenor, Boris Hofer, 
Señora Alderperson, Wilbraham Music (Chris Cox), June Cox, Rantz, Yuri Yerofeyev
