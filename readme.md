# Salvius

Salvius is a humanoid robot made from recycled materials. The robot is designed
to be as easy as possible for anyone to build on a limited budget.

> Salvius is a robot made out of recycled materials, designed to be able to
> perform a wide range of tasks by having a body structure that is similar
> to that of a human. The primary goal for Salvius is to create a humanoid
> robot that can function dynamically in a domestic environment.  
> ~ [salviusrobot.blogspot.com](http://salviusrobot.blogspot.com)

**Key features:**
  - Web based user interface
  - Easily customizable robots
  - RESTfull API
  - Modular design makes it easy to connect controllers via USB
  - [External status page](http://gunthercox.github.io/salvius.status/)

## Setup

Installing this software on your robot should be easy. Once you have downloaded 
the latest copy into a directory on your Rapsberry Pi, you can download and 
configure the robot's api and interface by running the following commands.

```
apt-get install pip
pip install -r requirements.txt
```

Use the following to run the robot's server.
```
python salvius.py runserver
```

**Note:** Code for the robot's Arduino boards can be found in the
[salvius.arduino](https://github.com/gunthercox/salvius.arduino) repository.
You will need to download the code to these boards individually and connect them
to the robot in order to enable these features.

### Text to speech

Salvius uses the [Emic 2 Text-to-Speech Module](https://www.sparkfun.com/products/11711)
to process text into verbal sounds. Code for controling this board is available
through the [salvius.arduino](https://github.com/gunthercox/salvius.arduino/tree/master/speech_synthesis) package.

### Speech recognition

This is still a bit of a work in progress, at best a few small words can be recognised.

### Handwriting

The robot can hold a pen and write when given a string of text.
The robot's handwriting is based on a grid in which each letter is created as a
result of horizontal and vertical lines.

### Communication

Salvius uses the [ChatterBot](https://github.com/gunthercox/ChatterBot) library
to reply to messages. This package also provides Salvius with the capability to
interact with people through social media sites.

### Object recognition

This includes face recognition, object tacking and learning to recognise new items.
Salvius currently does not have the ability to do this, however there is plans
to implement this in the future.

## Unit testing

The code for this project is automatically tested to ensure that it performs as
expected. These tests can also be run manually by running the command
```nosetests``` from within the repository's root directory. See 
([unit tests](http://en.wikipedia.org/wiki/Unit_testing)) for more information.

## Notes

#### SSH into Rapsberry Pi
- ```ssh pi@192.168.1.4``` (Your local ip may differ).
- The default password is ```password```.

#### Running on Pi from a flash drive
1. In Ubuntu `cd` into `/media/user_name/disk_name` to get to the content on the flash drive.
2. Log in to http://routerlogin.net/ to get a list of the ips of connected devices.
3. `ssh pi@192.168.1.2`
4. Mount the flash drive using `sudo mount -o uid=pi,gid=pi /dev/sda1 /mnt`
5. Then `cd` into `/mnt/salvius`
6. Run the server using `python salvius.py runserver`
7. In a browser navigate to `192.168.1.2:8000`

## Contributors
This project has been made possible with funding from the following sources:
Jennifer Cox, Adam Iredale, Janet Wise, Glen Zenor, Boris Hofer, 
Señora Alderperson, Wilbraham Music, Chris Cox, June Cox, Rantz, Yuri Yerofeyev
