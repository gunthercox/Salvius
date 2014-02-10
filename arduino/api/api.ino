/*
 * To use this demo,  enter one of the following USLs into your browser.
 * Replace "host" with the IP address assigned to the Arduino.
 *
 * http://host/
 * http://host/json
 *
 * This URL brings up a display of the values READ on digital pins 0-9
 * and analog pins 0-5.  This is done with a call to defaultCmd.
 * 
 * 
 * http://host/form
 *
 * This URL also brings up a display of the values READ on digital pins 0-9
 * and analog pins 0-5.  But it's done as a form,  by the "formCmd" function,
 * and the digital pins are shown as radio buttons you can change.
 * When you click the "Submit" button,  it does a POST that sets the
 * digital pins,  re-reads them,  and re-displays the form.
 * 
 */

#include "SPI.h"
#include "Ethernet.h"
#include "WebServer.h"
#include <Wire.h>

// no-cost stream operator as described at 
// http://sundial.org/arduino/?page_id=119
template<class T>
inline Print &operator <<(Print &obj, T arg)
{ obj.print(arg); return obj; }


// CHANGE THIS TO YOUR OWN UNIQUE VALUE
static uint8_t mac[] = { 0x90, 0xA2, 0xDA, 0x0D, 0x00, 0x8F };

// CHANGE THIS TO MATCH YOUR HOST NETWORK
static uint8_t ip[] = { 192, 168, 1, 177 };

#define PREFIX ""

WebServer webserver(PREFIX, 80);

// commands are functions that get called by the webserver framework
// they can read any posted data from client, and they output to server

void jsonCmd(WebServer &server, WebServer::ConnectionType type, char *url_tail, bool tail_complete)
{
  if (type == WebServer::POST)
  {
    server.httpFail();
    return;
  }

  //server.httpSuccess(false, "application/json");
  server.httpSuccess("application/json");
  
  if (type == WebServer::HEAD)
    return;

  int i;    
  server << "{ ";
  for (i = 0; i <= 9; ++i)
  {
    // ignore the pins we use to talk to the Ethernet chip
    int val = digitalRead(i);
    server << "\"d" << i << "\": " << val << ", ";
  }

  for (i = 0; i <= 5; ++i)
  {
    int val = analogRead(i);
    server << "\"a" << i << "\": " << val;
    if (i != 5)
      server << ", ";
  }
  
  server << " }";
}

void outputPins(WebServer &server, WebServer::ConnectionType type, bool addControls = false)
{
  P(htmlHead) =
    "<html>"
    "<head>"
    "<title>Arduino Web Server</title>"
    "<style type=\"text/css\">"
    "BODY { font-family: sans-serif }"
    "H1 { font-size: 14pt; text-decoration: underline }"
    "P  { font-size: 10pt; }"
    "</style>"
    "</head>"
    "<body>";

  int i;
  server.httpSuccess();
  server.printP(htmlHead);

  if (addControls)
    server << "<form action='" PREFIX "/form' method='post'>";

  server << "<h1>Digital Pins</h1><p>";

  for (i = 0; i <= 9; ++i)
  {
    // ignore the pins we use to talk to the Ethernet chip
    int val = digitalRead(i);
    server << "Digital " << i << ": ";
    if (addControls)
    {
      char pinName[4];
      pinName[0] = 'd';
      itoa(i, pinName + 1, 10);
      server.radioButton(pinName, "1", "On", val);
      server << " ";
      server.radioButton(pinName, "0", "Off", !val);
    }
    else
      server << (val ? "HIGH" : "LOW");

    server << "<br/>";
  }

  server << "</p><h1>Analog Pins</h1><p>";
  for (i = 0; i <= 5; ++i)
  {
    int val = analogRead(i);
    server << "Analog " << i << ": " << val << "<br/>";
  }

  server << "</p>";

  if (addControls)
    server << "<input type='submit' value='Submit'/></form>";

  server << "</body></html>";
}

void formCmd(WebServer &server, WebServer::ConnectionType type, char *url_tail, bool tail_complete)
{
  if (type == WebServer::POST)
  {
    bool repeat;
    char name[16], value[16];
    do
    {
      repeat = server.readPOSTparam(name, 16, value, 16);
      if (name[0] == 'd')
      {
        int pin = strtoul(name + 1, NULL, 10);
        int val = strtoul(value, NULL, 10);
        digitalWrite(pin, val);
      }
    } while (repeat);

    server.httpSeeOther(PREFIX "/form");
  }
  else
    outputPins(server, type, true);
}

void defaultCmd(WebServer &server, WebServer::ConnectionType type, char *url_tail, bool tail_complete)
{
  outputPins(server, type, false);  
}

void setup()
{
  // set pins 0-8 for digital input
  for (int i = 0; i <= 9; ++i)
    pinMode(i, INPUT);
  pinMode(9, OUTPUT);

  Ethernet.begin(mac, ip);
  webserver.begin();

  webserver.setDefaultCommand(&defaultCmd);
  webserver.addCommand("json", &jsonCmd);
  webserver.addCommand("form", &formCmd);
  
  // I2C Scanning
  Wire.begin();
  Serial.begin(9600);
  Serial.println("\nI2C Scanner");
}

void i2cScan()
{
 // --------------------------------------
// i2c_scanner
//
// Version 1
//    This program (or code that looks like it)
//    can be found in many places.
//    For example on the Arduino.cc forum.
//    The original author is not know.
// Version 2, Juni 2012, Using Arduino 1.0.1
//     Adapted to be as simple as possible by Arduino.cc user Krodal
// Version 3, Feb 26  2013
//    V3 by louarnold
// Version 4, March 3, 2013, Using Arduino 1.0.3
//    by Arduino.cc user Krodal.
//    Changes by louarnold removed.
//    Scanning addresses changed from 0...127 to 1...119,
//    according to the i2c scanner by Nick Gammon
//    http://www.gammon.com.au/forum/?id=10896
// Version 5, March 28, 2013
//    As version 4, but address scans now to 127.
//    A sensor seems to use address 120.
// 
//
// This sketch tests the standard 7-bit addresses
// Devices with higher bit address might not be seen properly.
//

/*
The sketch shows the 7-bit addresses of the found devices as 
hexadecimal values. That value can be used for the "Wire.begin" 
function which uses the 7-bit address. Some datasheets use the 
8-bit address and some example sketches use decimal addresses.
*/
  byte error, address;
  int nDevices;

  Serial.println("Scanning...");

  nDevices = 0;
  for(address = 1; address < 127; address++ ) 
  {
    // The i2c_scanner uses the return value of
    // the Write.endTransmisstion to see if
    // a device did acknowledge to the address.
    Wire.beginTransmission(address);
    error = Wire.endTransmission();

    if (error == 0)
    {
      Serial.print("I2C device found at address 0x");
      if (address<16) 
        Serial.print("0");
      Serial.print(address,HEX);
      Serial.println("  !");

      nDevices++;
    }
    else if (error==4) 
    {
      Serial.print("Unknow error at address 0x");
      if (address<16) 
        Serial.print("0");
      Serial.println(address,HEX);
    }    
  }
  if (nDevices == 0)
    Serial.println("No I2C devices found\n");
  else
    Serial.println("done\n");

  delay(5000);           // wait 5 seconds for next scan 
}

void loop()
{
  // process incoming connections one at a time forever
  webserver.processConnection();

  // if you wanted to do other work based on a connecton, it would go here
  //i2cScan();
}
