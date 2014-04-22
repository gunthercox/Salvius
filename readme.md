#Salvius

![Project photos](http://i.imgur.com/4sXpuA4.png)

[![Build Status](https://travis-ci.org/gunthercox/salvius.svg?branch=master)](https://travis-ci.org/gunthercox/salvius)

This repository contains the source code for Salvius, a robot who uses a 
Rapsberry Pi and several Arduino microcontrollers as a brain.

> Salvius is a robot made out of recycled materials
> and designed to be able to perform a wide range of
> tasks by having a body structure that is similar to
> that of a human. The primary goal for Salvius is to 
> create a humanoid robot that will be able to function
> dynamically in a domestic environment.

For additional details visit [salviusrobot.blogspot.com](http://salviusrobot.blogspot.com).

**Key features:** 
  - Web based user interface
  - RESTfull API
  - Modular design makes it easy to add controllers via I2C

## Setup
Installing this software on your robot should be easy. Once you have downloaded 
the latest copy into a directory on your Rapsberry Pi, you can download and 
configure the robot's api and interface by running the following three lines of code.

```
apt-get install pip
pip install -r requirements.txt
chmod a+x app.py
```

Use the following to run the robot's server.
```
python app.py runserver
```

## Features

### Text to speech
The robot uses a speech synthesis library to convert processed text into verbal sounds.
Checkout the repo for this library here: https://github.com/jscrane/TTS

### Speech recognition
This is still a bit of a work in progress, at best a few small words can be recognised.

### Communication experiment
I've included a package which allows the robot to tweet randomly selected 
messages to Twitter accounts. For now the robot cannot reply to users, however 
I have plans to add this feature. To use this feature you will need to register 
your app on https://dev.twitter.com/apps to get the token and secret keys. 
You will then need to create a file ```settings.py``` in the ```twitter``` 
directory with the following dictionary pointing to your Twitter keys and tokens.

```
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

## License
The MIT License (MIT)

Copyright (c) 2014 Gunther Cox

This project has been made possible with funding from the following sources:
Jennifer Cox, Adam Iredale, Janet Wise, Glen Zenor, Boris Hofer, 
Señora Alderperson, Wilbraham Music (Chris Cox), June Cox, Rantz, Yuri Yerofeyev

See http://salviusrobot.blogspot.com/2012/12/support-salvius.html for more information.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
