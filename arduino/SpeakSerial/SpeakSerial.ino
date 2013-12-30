
#include "TTS.h"

TTS tts(3);

void setup(void) {
  pinMode(13, OUTPUT);
}

void loop(void) {
  tts.sayText("robot is online");
}
