# Salvius Source Code
***

Salvius is an open source humanoid robot. For details about this project visit:
[http://salviusrobot.blogspot.com/p/about.html](http://salviusrobot.blogspot.com/p/about.html)

* The files in the www directory go on the robot's server.
* The java file in the interaction directory gets compiled as a jar and runs on the robots computer.
* The Arduino sketch in the arduino directory gets uploaded to the Arduino board.

## Server Setup:
I like to use a Ubuntu Server setup and these are just a few things that I do.
### These the packages I installed to setup my server environment
sudo apt-get install ssh gnome-core gdm php5 libapache2-mod-php5

## Arduino Setup:
* Plug Ethernet shield into Arduino Uno.
* Plug Seeed Relay Shield into Ethernet Shield.
* Attach 9 volt power supply to GND and +9V plugs of Relay Shield.
* PIR positive(+) to arduino 5V, PIR negative(-) to arduino GND, PIR OUT to HUB2 D3.
* Connect Ethernet shield to wireless router with Ethernet cable.

## License:
Author: Gunther Cox
Website: http://salviusrobot.blogspot.com

This project has been made possible with funding from the following individuals:
Jennifer Cox, Adam Iredale, Janet Wise, Glen Zenor, Boris Hofer, Señora Alderperson, Wilbraham Music (Chris Cox)

This work is licenced under Attribution-ShareAlike 3.0 Unported (CC BY-SA 3.0). Under this licence you are free to to Share, to copy, distribute and transmit the work
to Remix to adapt the work, to make commercial use of the work under the following conditions.

You must attribute this work as depicted in the copyright attributiuon of the code's comments but you may (but not in any way that suggests any endorsement of you or your use of the work.

If you alter, transform, or build upon this work, you may distribute the resulting work only under the same or similar license to this one.

Understand that any of the above conditions can be waived if you get permission from the copyright holder.

Where the work or any of its elements is in the public domain under applicable law, that status is in no way affected by the license.

In no way are any of the following rights affected by the license: Your fair dealing or fair use rights, or other applicable copyright exceptions and limitations; The author's moral rights; Rights other persons may have either in the work itself or in how the work is used, such as publicity or privacy rights.

Notice: For any reuse or distribution, you must not remove the attribution from these works.
