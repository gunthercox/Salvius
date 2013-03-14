# Salvius Source Code
***

Salvius is an open source humanoid robot. For details about this project visit:
[http://salviusrobot.blogspot.com](http://salviusrobot.blogspot.com)

## Server Setup:
I don't always set up servers but when I do, I choose Ubuntu.
This project runs on a Tomcat Java Server which you can choose during the initial installation of Ubuntu Server edition. It is also helpful to install OpenSSH at the same time.

* The files in the gui directory go on the robot's server.
* The java file in the interaction directory gets compiled as a jar and runs on the robots computer.
* The Arduino sketch in the arduino directory gets uploaded to the Arduino board.

## Arduino Setup:
* Plug Ethernet shield into Arduino Uno.
* Plug Seeed Relay Shield into Ethernet Shield.
* Attach 9 volt power supply to GND and +9V plugs of Relay Shield.
* PIR positive(+) to arduino 5V, PIR negative(-) to arduino GND, PIR OUT to HUB2 D3.
* Connect Ethernet shield to wireless router with Ethernet cable.

## License:
Author: Gunther Cox
Website: http://salviusrobot.blogspot.com

This project has been made possible with funding from the following businesses and individuals:
Jennifer Cox, Adam Iredale, Janet Wise, Glen Zenor, Boris Hofer, Señora Alderperson, Wilbraham Music (Chris Cox), June Cox

This work is licenced under Attribution-ShareAlike 3.0 Unported (CC BY-SA 3.0). Under this licence you are free to to Share, to copy, distribute and transmit the work
to Remix to adapt the work, to make commercial use of the work under the following conditions.

You must attribute this work as depicted in the copyright attribution of the code's comments but you may (but not in any way that suggests any endorsement of you or your use of the work.

If you alter, transform, or build upon this work, you may distribute the resulting work only under the same or similar license to this one.

Understand that any of the above conditions can be waived if you get permission from the copyright holder.

Where the work or any of its elements is in the public domain under applicable law, that status is in no way affected by the license.

In no way are any of the following rights affected by the license: Your fair dealing or fair use rights, or other applicable copyright exceptions and limitations; The author's moral rights; Rights other persons may have either in the work itself or in how the work is used, such as publicity or privacy rights.

Notice: For any reuse or distribution, you must not remove the attribution from these works.
