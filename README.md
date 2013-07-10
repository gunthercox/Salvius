# Open Source Humanoid Robot

####Salvius is an open source humanoid robot. For additional details visit:

The main idea that I am attempting to promote is onboard expirimental development. My goal is to create this software
so that I, and anyone else who needs it can develop and make changes to a robot's programming rapidly, and without
having to plug in via a tethered connection. My web interface also is designed to contain many usefull control, and
diagnostic tools.

## Server Setup:
I don't always set up servers but when I do, I choose Ubuntu.
* Install or use a copy of Ubuntu Server edition. It is also helpful to install OpenSSH at the same time.
* On the server it is helpfull to install OpenSSH, git, and nginx.
* Configureing nginx is wicked easy, just edit etc/nginx/nginx.conf

```

```

Install the robots web ui by cloning this git repository.
```
cd usr/share/nginx/www/
git clone https://github.com/gunthercox/Salvius.git
```

After you make changes to files on the server you should restart nginx.
```
sudo service nginx restart
```

* The files in the gui directory go on the robot's server.
* The java file in the interaction directory gets compiled as a jar and runs on the robots computer.
* The Arduino sketch in the arduino directory gets uploaded to the Arduino board.

## Arduino Setup:
* Plug Ethernet shield into Arduino Uno.
* Plug Seeed Relay Shield into Ethernet Shield.
* Attach 9 volt power supply to GND and +9V plugs of Relay Shield.
* PIR positive(+) to arduino 5V, PIR negative(-) to arduino GND, PIR OUT to HUB2 D3.
* Connect Ethernet shield to wireless router with Ethernet cable.

## Development: [![Build Status](https://travis-ci.org/gunthercox/Salvius.png?branch=master)](https://travis-ci.org/gunthercox/Salvius)

I am currently working on implementing AJSON to interact with the arduino boards via api. This will be much simpler and
more efficient than using the java library.

Check out what the interface looks like on the gh-pages branch: [http://gunthercox.github.io/Salvius/](http://gunthercox.github.io/Salvius/)

### Tools and libraries included in this project
* [angularjs](http://angularjs.org)
* [Foundation UI](http://foundation.zurb.com)
* [DropzoneJS](http://www.dropzonejs.com)
* [d3.js](http://d3js.org)
* [OneGate](https://github.com/liftoff/GateOne) [Wikipedia](http://en.wikipedia.org/wiki/Web-based_SSH)

#### Packages
* [nginx](http://wiki.nginx.org)
* [nodejs](http://nodejs.org)
* [express](http://expressjs.com/)
* [component](https://github.com/component/component)

You can install required packages for this project by running the following
```
sudo apt-get install nginx
```

For installing node.js and npm there is wonderfull script that works, just download and run it.
I have also included express in this install
```
wget https://npmjs.org/install.sh
sudo sh install.sh
sudo npm install express
sudo npm install component
```
## License:
This work is GPL-3.0
@author: Gunther Cox
@website: http://salviusrobot.blogspot.com

This project has been made possible with funding from the following businesses and individuals:
Jennifer Cox, Adam Iredale, Janet Wise, Glen Zenor, Boris Hofer, Señora Alderperson, Wilbraham Music (Chris Cox),June Cox, Rantz
