// Programmer: Gunther Cox
// http://salviusrobot.blogspot.com
// Created: 12/25/11
// Last Modified: 12/25/11
// Hardware setup instructions:
// Plug relay shield directly into arduino so that all pins line up.
// Attach 9 volt power supply to GND and +9V plugs of relay shield.
// PIR + to arduino 5V, PIR - to arduino GND, PIR OUT to HUB2 D3.

int relayPin1 = 4; // relay connected to digital pin 4 (D3 on relay shield)
int relayPin2 = 5; // relay connected to digital pin 5 (D2 on relay shield) (not used)
int relayPin3 = 6; // relay connected to digital pin 6 (D1 on relay shield) (not used)
int relayPin4 = 7; // relay connected to digital pin 7 (D0 on relay shield) (not used)
int pirPin = 3;  // choose the input pin (for PIR sensor)
int pirState = LOW; // we start, assuming no motion detected 
int val;            // variable for reading the pin status
int pirMode = 0;    // determines if the relay closed already (0 = not closed yet)

void setup() {
  //the time we give the sensor to calibrate (10-60 secs according to the datasheet)
  pinMode(pirPin, INPUT);        // declare sensor as input
  pinMode(relayPin1, OUTPUT);    // declare relay as output
  digitalWrite(relayPin1, LOW);
  digitalWrite(pirPin, LOW);
  pirState = digitalRead(pirPin); // read the initial state
  delay(60000);                   // pause before calibrating 
}

void loop() {
  val = digitalRead(pirPin);  // read input value and store it in val
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
}

