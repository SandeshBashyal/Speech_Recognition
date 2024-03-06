#include<Servo.h>

const int inP1A = 9;
const int inP2A = 11;  

Servo servoForDoor;

void setup() {
  pinMode(inP1A, OUTPUT);
  pinMode(inP2A, OUTPUT);

  servoForDoor.attach(3);

}

void loop() {
  // Motors will spin in the set direction at the specified speed.
  //Use analogWrite() to control the speed (PWM)
  digitalWrite(inP1A, HIGH);  // Motor A full speed
  digitalWrite(inP2A, LOW);
  
   //Using servo motor
  
  servoForDoor.write(0);
  delay(1000);
  servoForDoor.write(90);
  delay(1000);
  servoForDoor.write(180);
  delay(1000);
  

}

