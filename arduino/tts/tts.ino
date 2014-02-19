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

// digital pin 13
#define ledPin 13

char text [50];
boolean state = 0;

// speech output is digital pin 10
TTS text2speech;

void Test_Speech() {
  // higher values = lower voice pitch
  text2speech.setPitch(16);
  
  strcpy(text, "This is a test how are you doing I am a robot");
  text2speech.say(text);
}

// function that executes whenever data is received from master
// this function is registered as an event, see setup()
void receiveEvent(int howMany) {
  String x = String(Wire.read());    // receive byte as an integer
    Serial.println(x);
}

void setup() {
  pinMode(ledPin, OUTPUT);
  
  Serial.begin(9600);
  Serial.println("Slave online");
  
  // join i2c bus with address #4
  Wire.begin(4);
  
  // register event
  Wire.onReceive(receiveEvent);
}

void loop() {
  
  // slave may send less than requested
  while(Wire.available())
  {
    // receive a byte as character
    char c = Wire.read();
    Serial.print(c);
    delay(1000);
  }
  
  while(Wire.available() == false)
  {
  state = !state;
  digitalWrite(ledPin, state);
  Test_Speech();
  delay(1000);
  }
}

