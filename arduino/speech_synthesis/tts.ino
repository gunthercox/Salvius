/*
  Text To Speech syntesis library
 Copyright (c) 2008 Clive Webster.  All rights reserved.
 Nov. 29th 2009 - Modified to work with Arduino by Gabriel Petrut.
 The Text To Speech library uses Timer1 to generate the PWM
 output on digital pin 10. The output signal needs to be fed
 to an RC filter then through an amplifier to the speaker.
 */

#include <Wire.h>
#include "TTS.h"

char text [50];

// String to store text which needs to be spoken
String buffer = "";

// speech output is digital pin 10
TTS text2speech;

void Test_Speech(char input []) {
  // higher values = lower voice pitch
  text2speech.setPitch(16);
  
  strcpy(text, input);
  text2speech.say(text);
}

// This event function executes whenever data is received from master
void receiveEvent(int byteCount) {
  while(Wire.available())
  {
    // receive a byte as character
    char c = Wire.read();
    buffer += c;
  }
}

void setup() {
  
  Serial.begin(9600);
  Serial.println("Slave online");
  
  // join i2c bus with address #4
  Wire.begin(4);
  
  // register event
  Wire.onReceive(receiveEvent);
}

void loop() {
  
  while(Wire.available() == false)
  {
  
  Serial.print(buffer);
    if (buffer != "") {
      // Convert string to char array
      char item[50];
      buffer.toCharArray(item, 50);
      
      Test_Speech(item);
      
      // The text has been spoken so clear the buffer
      buffer = "";
    }
  }
  
  delay(1000);
}


