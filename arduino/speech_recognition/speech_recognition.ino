#include "uspeech.h"

#define led 13

signal voice(A0);
char prev;

void setup(){
  voice.f_enabled = true;
  voice.minVolume = 1000;
  voice.fconstant = 400;
  voice.econstant = 1;
  voice.aconstant = 2;
  voice.vconstant = 3;
  voice.shconstant = 4;
  voice.calibrate();
  Serial.begin(9600);
  pinMode(led, OUTPUT); 
}

void loop(){
    voice.sample();
    char p = voice.getPhoneme();
    
    if (p != prev) {
      Serial.println(p);
    }
      
    if(p!=' ') {
      if((p=='v')) {
          digitalWrite(led, HIGH);
      } else {
          
          digitalWrite(led, LOW);
      }
    }
    prev = p;
}
