// Wire Master Writer
#include <Wire.h>
byte x = 0;

// MOTOR CONTROLER
int pinI1=8;//define I1 interface
int pinI2=11;//define I2 interface 
int speedpinA=9;//enable motor A
int pinI3=12;//define I3 interface 
int pinI4=13;//define I4 interface 
int speedpinB=10;//enable motor B
int spead =500;//define the spead of motor


// CONVERT STRING INTO CHARACTER ARRAY
//char letter[3] = {'A', 'B', 'C'};
//text.toCharArray(letter, 3);

// TEMP SENSOR
/*int a;
 int del=1000; // duration between temperature readings
 float temperature;
 int B=3975; 
 float resistance;*/

// GET A STRING FROM SERIAL PORT
// SKIP THIS FOR NOW AND JUST USE THE FOLLOWING STRING
String text = "abc";

void setup() {
  pinMode(pinI1, OUTPUT);
  pinMode(pinI2, OUTPUT);
  pinMode(speedpinA, OUTPUT);
  pinMode(pinI3, OUTPUT);
  pinMode(pinI4, OUTPUT);
  pinMode(speedpinB, OUTPUT);
  Wire.begin(); // join i2c bus (address optional for master)

  // START COMMUNICATION
  Serial.begin(9600); 
}

void forward() {
  analogWrite(speedpinA,spead);//input a simulation value to set the speed
  analogWrite(speedpinB,spead);
  digitalWrite(pinI4,HIGH);//turn DC Motor B move clockwise
  digitalWrite(pinI3,LOW);
  digitalWrite(pinI2,HIGH);//turn DC Motor A move anticlockwise
  digitalWrite(pinI1,LOW);
}
void backward() {
  analogWrite(speedpinA,spead);//input a simulation value to set the speed
  analogWrite(speedpinB,spead);
  digitalWrite(pinI4,LOW);//turn DC Motor B move anticlockwise
  digitalWrite(pinI3,HIGH);
  digitalWrite(pinI2,LOW);//turn DC Motor A move clockwise
  digitalWrite(pinI1,HIGH);
}
void left() {
  Wire.beginTransmission(4); // transmit to device #4
  Wire.write(x);              // sends one byte  
  Wire.endTransmission();    // stop transmitting
  delay(500);
}
void right() {
  Wire.beginTransmission(4); // transmit to device #4
  Wire.write(x);              // sends one byte  
  Wire.endTransmission();    // stop transmitting
  delay(500);
}
void stop() {
  // Unenble the pin, to stop the motor. This should be done to avid damaging the motor
  digitalWrite(speedpinA,LOW);
  digitalWrite(speedpinB,LOW);
  delay(500);
}

int serialData = 0;

void loop() {

  // RESPOND ONLY WHEN RECIEVING DATA
  if (Serial.available()) {

    // READ INCOMING BYTE  
    char ser = Serial.read();

    if (ser == '1') {
      forward();
      delay(50);
      stop();
    } 
    else if (ser == '2') {
      backward();
      delay(50); 
      stop();
    } 
    else if (ser == '3') {
      right();
      delay(50);
      stop();
    } 
    else {
      delay(50); 
    }
  }

}

// SEND TEMPERATURE READING
/*a=analogRead(0);
 resistance=(float)(1023-a)*10000/a; 
 temperature=1/(log(resistance/10000)/B+1/298.15)-273.15;
 delay(del);
 Serial.println(temperature);*/

