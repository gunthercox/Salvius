/*
* Author: Gunther Cox
* CC: Salvius Robot Project
* Website: http://salviusrobot.blogspot.com
*
* This project has been made possible with funding from the following individuals:
* Jennifer Cox, Adam Iredale, Janet Wise, Glen Zenor, Boris Hofer, Derek White, Nick Nault, 
* Señora Alderperson, Wilbraham Music (Chris Cox)
*/

// FOR ETHERNET
#include <Ethernet.h>
#include <SPI.h>

#include <Client.h>
#include <Server.h>
#include <Udp.h>

// VARIABLES FOR MANUAL SETUP
byte mac[] = { 
  0x90, 0xA2, 0xDA, 0x0D, 0x00, 0x8F }; // physical mac address
byte ip[] = { 
  192, 168, 1, 177 };      // ip in lan
byte gateway[] = { 
  192, 168, 0, 1 };        // internet access via router
byte subnet[] = { 
  255, 255, 255, 0 };      //subnet mask
EthernetServer server(80);

//int pirPin = 3;  // PIR SENSOR
int relayPin1 = 4; // relay connected to digital pin 4 (D3 on relay shield - on switch)
int relayPin2 = 7; // relay connected to digital pin 5 (D2 on relay shield) - Inferred LEDs
int relayPin3 = 6; // relay connected to digital pin 6 (D1 on relay shield) - Ultraviolte LEDs
int relayPin4 = 5; // relay connected to digital pin 7 (D0 on relay shield) (not used)
//pin 10 - RESERVED FOR ETHERNET SHIELD
//pin 11 - RESERVED FOR ETHERNET SHIELD
//pin 12 - RESERVED FOR ETHERNET SHIELD
//pin 13 - RESERVED FOR ETHERNET SHIELD

// STORES URL DATA
String readString = String(30);

// STATUS FLAGS
boolean FORWARD = false;
boolean BACKWARD = false;
boolean LEFT = false;
boolean RIGHT = false;
boolean LEDON = false;
boolean LED2ON = false;

void setup(){
  // Start Ethernet
  Ethernet.begin(mac, ip, gateway, subnet);
  pinMode(relayPin3, OUTPUT);  //Set pin 7 to output
  pinMode(relayPin4, OUTPUT);

  //  pinMode(pirPin, INPUT);        // declare sensor as input
  pinMode(relayPin1, OUTPUT);    // declare relay1 as output
  pinMode(relayPin2, OUTPUT);    // declare relay2 as output
  pinMode(relayPin3, OUTPUT);    // declare relay3 as output
  pinMode(relayPin4, OUTPUT);    // declare relay4 as output

  /*digitalWrite(relayPin1, LOW);
   digitalWrite(pirPin, LOW);
   pirState = digitalRead(pirPin); // read the initial state
   delay(60000);                   // pause before calibrating
   */
}

void loop(){
  // Create a client connection
  EthernetClient client = server.available();
  if (client) {
    while (client.connected()) {
      if (client.available()) {
        char c = client.read();
        //read char by char HTTP request
        if (readString.length() < 100) {
          readString += c; //store characters to string
        }

        if (c == '\n') {  //if HTTP request has ended

          //dirty skip of "GET /favicon.ico HTTP/1.1"
          if (readString.indexOf("?") <0) { /*skip everything*/
          }

          else

            // BEGIN DRIVE CONTROL
          if(readString.indexOf("N1=Forward") >0) {

            // ITEM HAS TO BE TURNED ON
            digitalWrite(relayPin1, HIGH);    // set the item on
            FORWARD = true;
          }

          else {
            
            // ITEM HAS TO BE TURNED OFF
            digitalWrite(relayPin1, LOW);    // set the item off
            FORWARD = false;           
          }

          if (readString.indexOf("N2=BACKWARD") > 0) {
            //item has to be turned ON
            digitalWrite(relayPin2, HIGH);    // set the item on
            BACKWARD = true;
          }
          else {
            //item has to be turned OFF
            digitalWrite(relayPin2, LOW);    // set the item off
            BACKWARD = false;           
          }

          if (readString.indexOf("N3=LEFT") > 0) {
            //item has to be turned ON
            digitalWrite(relayPin3, HIGH);    // set the item on
            LEFT = true;
          }
          else {
            //item has to be turned OFF
            digitalWrite(relayPin3, LOW);    // set the item off
            LEFT = false;           
          }

          if (readString.indexOf("N4=RIGHT") > 0) {
            //item has to be turned ON
            digitalWrite(relayPin4, HIGH);    // set the item on
            RIGHT = true;
          }
          else {
            //item has to be turned OFF
            digitalWrite(relayPin4, LOW);    // set the item off
            RIGHT = false;           
          }
          // end drive control

          //lets check if LED should be lighted
          if (readString.indexOf("L=ON") >0) {
            //led has to be turned ON
            digitalWrite(relayPin3, HIGH);    // set the LED on
            LEDON = true;
          }
          else if (readString.indexOf("L2=ON") >0) {
            //led has to be turned ON
            digitalWrite(relayPin4, HIGH);    // set the LED on
            LED2ON = true;
          }
          //led has to be turned OFF
          else {
            //led has to be turned OFF
            digitalWrite(relayPin4, LOW);    // set the LED OFF
            LED2ON = false;
            digitalWrite(relayPin3, LOW);    // set the LED OFF
            LEDON = false;
          }

          // now output HTML data starting with standart header
          client.println("HTTP/1.1 200 OK");
          client.println("Content-Type: text/html");
          client.println();
          client.println("<body><link href='http://192.168.1.2/bootstrap/css/bootstrap.css' rel='stylesheet'>");

          client.println("<form method=get name=NAV>");
          client.println("<input type=submit name=N1 value=FORWARD>");
          client.println("<input type=submit name=N3 value=LEFT><input type=submit value=STOP><input type=submit name=N4 value=RIGHT>");
          client.println("<input type=submit name=N2 value=BACKWARD>");

          //controlling leds via buttons (address will look like http://192.168.1.177/?L=ON when submited)
          if (LEDON)
            client.println("<form method=get name=LED><input type=submit value=OFF></form>");
          else
            client.println("<form method=get name=LED><input type=submit name=L value=ON></form>");

          if (LED2ON)  // begin second LED
            client.println("<td align=center><form method=get name=LED2><input type=submit value=OFF></form></td></tr>");
          else
            client.println("<form method=get name=LED2><input type=submit name=L2 value=ON></form>");
          client.println("</form>");

          // Begin print drive status
          if (FORWARD)
            client.println("DRIVING FORWARD");

          else if (BACKWARD)
            client.println("DRIVING BACKWARD");

          else if (LEFT)
            client.println("TURNING LEFT");

          else if (RIGHT)
            client.println("TURNING RIGHT");

          else
            client.println("PROBABLY NOT DRIVING");
          // End print drive status

          //printing LED status
          client.print("LED status: ");
          if (LEDON)
            client.println("<font color='purple' size='4'>ULTRAVIOLET ON</font>");

          else if (LED2ON)
            client.println("<font color='red' size='4'>INFERRED ON</font>");

          else
            client.println("<font color='grey' size='4'>OFF</font>"); 
          // end second LED

          client.println("</body></html>");
          //clearing string for next read
          readString="";
          //stopping client
          client.stop();
        }
      }
    }
  }
}

// auto-activation function
void autoActivat() {
  // Begin variables for motion sensor (these were at the top)
  int pirState = LOW; // we start, assuming no motion detected
  int val;            // variable for reading the pin status
  int pirMode = 0;    // determines if the relay closed already (0 = not closed yet)
  // End variabled for motion sensor

  /*val = digitalRead(pirPin);  // read input value and store it in val
  if(digitalRead(pirPin) == HIGH) {
    if (pirMode == 0) {
      if (val != pirState) {            //look for 2 inconsistant readings
        // turn main computer on
        digitalWrite(relayPin1, HIGH);  // sets relay1 on
        delay(1000);                    // waits for 1 second
        digitalWrite(relayPin1, LOW);   // sets relay1 off
        pirMode = pirMode + 1;   // relay has been on     
        //delay(50);
      }     
    }
  }
  */
}


