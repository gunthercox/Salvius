# Open Source Humanoid Robot

Salvius is an open source humanoid robot. For details about this project visit:
[http://salviusrobot.blogspot.com](http://salviusrobot.blogspot.com)

***

## Server Setup:
I don't always set up servers but when I do, I choose Ubuntu.
This project runs on a Tomcat Java Server which you can choose during the initial installation of Ubuntu Server edition. It is also helpful to install OpenSSH at the same time.

* The files in the gui directory go on the robot's server.
* The java file in the interaction directory gets compiled as a jar and runs on the robots computer.
* The Arduino sketch in the arduino directory gets uploaded to the Arduino board.

***

## Arduino Setup:
* Plug Ethernet shield into Arduino Uno.
* Plug Seeed Relay Shield into Ethernet Shield.
* Attach 9 volt power supply to GND and +9V plugs of Relay Shield.
* PIR positive(+) to arduino 5V, PIR negative(-) to arduino GND, PIR OUT to HUB2 D3.
* Connect Ethernet shield to wireless router with Ethernet cable.

***

## Development:
~~I have recently added the rxtx-2.1-7r2 library written mostly in java to this repository. The rxtx-2.1-7r2 library is
the same one that is used in the Arduino IDE to allow the computer to communicate with the Arduino board through the
serial port. I hope to use this library to allow a developer to access and make modifications to the microcontroller's
code directly from the web interface on the robot's server.~~

Note: If editing this code in eclipse make sure to set up tomcat in the build path:
Right click on project ---> Properties ---> Java Build Path ---> Add Library... ---> Server Runtime ---> Apache Tomcat

Note: When deploying to Tomcat using the manager webapp you should first configure a username and password:
Edit etc/tomcat7/tomcat-users.xml as shown bellow. Change USERNAME and PASSWORD to what you want.

```
<?xml version='1.0' encoding='utf-8'?>  
<tomcat-users>  
  <role rolename="tomcat"/>  
  <role rolename="role1"/>  
  <role rolename="manager"/>  
  <user username="tomcat" password="tomcat" roles="tomcat"/>  
  <user username="both" password="tomcat" roles="tomcat,role1"/>  
  <user username="role1" password="tomcat" roles="role1"/>  
  <user username="USERNAME" password="PASSWORD" roles="manager,tomcat,role1"/>  
</tomcat-users>  
```

Note: If you make changes to a file you should restart Tomcat:
/etc/init.d/tomcat7 start
/etc/init.d/tomcat7 stop
/etc/init.d/tomcat7 restart

### Tools and libraries included in this project
* [Foundation UI](http://foundation.zurb.com/)
* Tomcat7

The main idea that I am attempting to promote is onboard expirimental development. My goal is to create this software
so that I, and anyone else who needs it can develop and make changes to a robot's programming rapidly, and without
having to plug in via a tethered connection. My web interface also is designed to contain many usefull control, and
diagnostic tools.

***

## License:
@author: Gunther Cox
@website: http://salviusrobot.blogspot.com

This project has been made possible with funding from the following businesses and individuals:
Jennifer Cox, Adam Iredale, Janet Wise, Glen Zenor, Boris Hofer, Señora Alderperson, Wilbraham Music (Chris Cox), June Cox, Rantz

This work is licenced under Attribution-ShareAlike 3.0 Unported (CC BY-SA 3.0). Under this licence you are free to to Share, to copy, distribute and transmit the work
to Remix to adapt the work, to make commercial use of the work under the following conditions.

You must attribute this work as depicted in the copyright attribution of the code's comments but you may (but not in any way that suggests any endorsement of you or your use of the work.

If you alter, transform, or build upon this work, you may distribute the resulting work only under the same or similar license to this one.

Understand that any of the above conditions can be waived if you get permission from the copyright holder.

Where the work or any of its elements is in the public domain under applicable law, that status is in no way affected by the license.

In no way are any of the following rights affected by the license: Your fair dealing or fair use rights, or other applicable copyright exceptions and limitations; The author's moral rights; Rights other persons may have either in the work itself or in how the work is used, such as publicity or privacy rights.

Notice: For any reuse or distribution, you must not remove the attribution from these works.
