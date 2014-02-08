/*
  Text To Speech syntesis library
  Copyright (c) 2008 Clive Webster.  All rights reserved.
  Nov. 29th 2009 - Modified to work with Arduino by Gabriel Petrut.
*/

/*
  The Text To Speech library uses Timer1 to generate the PWM
  output on digital pin 10. The output signal needs to be fed
  to an RC filter then through an amplifier to the speaker.
*/

#ifndef TTS_h
#define TTS_h

#include <Arduino.h>
#include <inttypes.h>
#include "english.h"

class TTS
{
  private:

  public:
    TTS();
    void say(const char * );
    void speak(const char * );
    void setPitch(byte pitch);
};

#endif
