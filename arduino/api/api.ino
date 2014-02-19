/*
 *
 * http://host/
 *
 * This URL brings up a display of the values READ on digital pins 0-9
 * and analog pins 0-5.  This is done with a call to defaultCmd.
 * 
 * http://host/json
 * 
 */

#include <SPI.h>
#include <Ethernet.h>
#include <Wire.h>
#include "WebServer.h"
#include "settings.h"

// no-cost stream operator as described at 
// http://sundial.org/arduino/?page_id=119
template<class T>
inline Print &operator <<(Print &obj, T arg)
{ obj.print(arg); return obj; }

WebServer webserver(PREFIX, 80);

void jsonCmd(WebServer &server, WebServer::ConnectionType type, char *url_tail, bool tail_complete)
{
  server.httpSuccess();
  
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
      // If this is a speech item
      if (String(name).equals("say")) {
        // CURRENTLY JUST A TEST TO PRINT THE VALUE TO SERIAL
        Serial.println("master:");
        Serial.println(String(value));
        send_string(value, text_to_speech_i2c_address);
      }
    } while (repeat);

    return;
  }
  
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
    server << "\"a" << i << "\": " << val << ", "; 
  }
  
  // CUSTOM SENSOR OUTPUTS
  server << "\"temperature" << "\": " << temperature_sensor(0);
  
  server << " }";
}

void outputPins(WebServer &server, WebServer::ConnectionType type)
{
  // IF EMPTY BRACKETS ARE RETURNED, THEN THERE IS NO I2C DEVICES
  
  byte error, address;
  int nDevices = 0;
  nDevices = 0;

  server.httpSuccess("application/json");
  server << "{ ";
  
  for(address = 1; address < 127; address++ ) 
  {
    /* The i2c_scanner uses the return value of 
    the Write.endTransmisstion to see if
    a device did acknowledge to the address.*/
        
    Wire.beginTransmission(address);
        
    /*
    There is an issue with the arduino wire library in which
    it will stop the code if an i2c device looses power.
    This issue does not affect the prefrmance of this code if
    there is no i2c devices connected.
    http://forum.arduino.cc/index.php/topic,37822.0.html
    */
    
    if (error == 0)
    {
      server << "\"i2c" << "\": " << "0x";
      if (address<16) {
        server << "0";
      }
      server << address << HEX << ", ";
      nDevices++;
    }
    if (error==4) 
    {
      server << "\"error" << "\": " << "0x";
      if (address<16) {
        server << "0";
      }
      server << address << HEX;
      return;
    }    
  }

  server << " }";
}

float temperature_sensor(int pin) {
  // READ GROVE I2C TEMPERATURE SENSOR
  const int B=3975;
  int a=analogRead(pin);
  float resistance=(float)(1023-a)*10000/a;
  float temperature=1/(log(resistance/10000)/B+1/298.15)-273.15;
  return temperature;
}

void send_string(char string[], int address) {
 /*
 Send a string to an i2c address.
 */
 Wire.beginTransmission(address);
 Wire.write(string);
 Serial.println("String: " + String(string));
 Wire.endTransmission();
}

void i2cCmd(WebServer &server, WebServer::ConnectionType type, char *url_tail, bool tail_complete)
{
    outputPins(server, type);
}

void setup()
{
  // set pins 0-8 for digital input
  for (int i = 0; i <= 9; ++i)
    pinMode(i, INPUT);
  pinMode(9, OUTPUT);
  //pin 10 - RESERVED FOR ETHERNET SHIELD
  //pin 11 - RESERVED FOR ETHERNET SHIELD
  //pin 12 - RESERVED FOR ETHERNET SHIELD
  //pin 13 - RESERVED FOR ETHERNET SHIELD

  Ethernet.begin(mac, ip);
  webserver.begin();

  webserver.setDefaultCommand(&jsonCmd);
  webserver.addCommand("i2c", &i2cCmd);
  
  // I2C and Serial
  Wire.begin();
  Serial.begin(9600);
  Serial.println("master online");
}

void loop()
{
  // process incoming connections one at a time forever
  webserver.processConnection();

  // start any additional work here
}
