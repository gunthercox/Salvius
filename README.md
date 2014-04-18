# Open Source Humanoid Robot

####Salvius is an open source humanoid robot. For additional details visit: [salviusrobot.blogspot.com](http://salviusrobot.blogspot.com)
[Bill of Materials](http://salviusrobot.blogspot.com/p/resources.html)

The main idea that I am attempting to promote is onboard expirimental development. My goal is to create this software
so that I, and anyone else who needs it can develop and make changes to a robot's programming rapidly, and without
having to plug in via a tethered connection. My web interface also is designed to contain many usefull control, and
diagnostic tools.

## Server Setup:
I don't always set up servers but when I do, I choose Ubuntu.
* Install or use a copy of Ubuntu Server edition. It is also helpful to install OpenSSH at the same time.
* On the server it is helpfull to install OpenSSH, git, and nginx.
* Configureing nginx is wicked easy, just edit etc/nginx/nginx.conf and add the following just beffore the closing bracket

```
server {
        listen 80;
        server_name _;
        location / {
                root /usr/share/nginx/www;
                index index.html index.htm;
        }
}
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

Check out what the interface looks like on the gh-pages branch: [http://gunthercox.github.io/Salvius/](http://gunthercox.github.io/Salvius/)

### Tools and libraries included in this project
* [Foundation UI](http://foundation.zurb.com)
* [DropzoneJS](http://www.dropzonejs.com)
* [hQuery Knob](http://anthonyterrien.com/knob/)
* [d3.js](http://d3js.org)

#### Packages
* [nginx](http://wiki.nginx.org)

You can install required packages for this project by running the ```./setup.sh``` file.

## License:
This work is GPL-3.0
@author: Gunther Cox
@website: http://salviusrobot.blogspot.com
The characteristics and/or functions of the robot are subject to changes without prior notice.

This project has been made possible with funding from the following sources:
Jennifer Cox, Adam Iredale, Janet Wise, Glen Zenor, Boris Hofer, Señora Alderperson, Wilbraham Music (Chris Cox), June Cox, Rantz, Yuri Yerofeyev
