Salvius
=========

This repository contains the source code for Salvius, a robot who uses a Rapsberry Pi and several Arduino microcontrollers as a brain.

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

## Setup
Installing this software on your robot should be easy. Once you have downloaded the latest copy into a directory on your Rapsberry Pi, you can download and configure the robot's api and interface by running the following three lines of code.
```
sudo apt-get install pip
pip install -r requirements.txt
chmod a+x app.py
```

Use the following to run the robot's server.
```
python app.py runserver
```

## Features
I've included a package which allows the robot to tweet randomly selected messages to Twitter accounts. For now the robot cannot reply to tweets, however I have plans to add this feature soon.
If you want to use this program you will need to register your app on https://dev.twitter.com/apps to get the token and secret keys. You will then need to create a file ```settings.py``` in the ```twitter``` directory with the following variables pointing to your Twitter keys and tokens.

```
CONSUMER_KEY = ""
CONSUMER_SECRET = ""
TOKEN = ""
TOKEN_SECRET = ""
```

## License:
This work is licensed MIT free by Gunther Cox

This project has been made possible with funding from the following sources:
Jennifer Cox, Adam Iredale, Janet Wise, Glen Zenor, Boris Hofer, Señora Alderperson, Wilbraham Music (Chris Cox), June Cox, Rantz, Yuri Yerofeyev

_The characteristics and/or functions of the robot are subject to changes without prior notice._

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
