// Wire Slave Receiver
#include <Wire.h>

void setup() {
  Serial.begin(9600);
  Serial.println("Slave online");
  
  Wire.begin(4);                // join i2c bus with address #4
  Wire.onReceive(receiveEvent); // register event
}

void loop() {
  while(Wire.available())    // slave may send less than requested
  { 
    char c = Wire.read();    // receive a byte as character
    Serial.print(c);         // print the character
  }
  delay(1000);
}

// function that executes whenever data is received from master
// this function is registered as an event, see setup()
void receiveEvent(int howMany) {
  String x = String(Wire.read());    // receive byte as an integer
    Serial.println(x);
}
