// Wire Slave Receiver
#include <Wire.h>

unsigned char relayPin[4] = {4,5,6,7};

void setup() {
  Wire.begin(4);                // join i2c bus with address #4
  Wire.onReceive(receiveEvent); // register event
  for(int i = 0; i < 4; i++) {
    pinMode(relayPin[i], OUTPUT);
  }
}

void loop() {
  delay(1000);
}

// function that executes whenever data is received from master
// this function is registered as an event, see setup()
void receiveEvent(int howMany) {
  int x = Wire.read();    // receive byte as an integer
    if (x == 0) {
    digitalWrite(relayPin[1], HIGH);
    delay(500);
    digitalWrite(relayPin[1], LOW);
    delay(1000);
  }
}
