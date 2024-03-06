#include <Servo.h>

const int inP1A = 9;
const int inP2A = 11;
const int lightPin1 = 2;
const int relayPin2 = 13;

 
Servo servoForDoor;

char userInput;

void setup(){
  pinMode(inP1A, OUTPUT);
  pinMode(inP2A, OUTPUT);
  pinMode(lightPin1, OUTPUT);
  pinMode(relayPin2, OUTPUT);
  
  servoForDoor.attach(3);
  servoForDoor.write(55);
  Serial.begin(9600);
}

void loop(){
  if(Serial.available()>0){
    userInput = Serial.read();
    digitalWrite(lightPin1, HIGH);
    delay(50);
    digitalWrite(lightPin1, LOW);

  }


  if(userInput == 'A'){
    digitalWrite(lightPin1, HIGH);
 //     digitalWrite(rLightPin1, HIGH);
  }


  if(userInput == 'B'){
    digitalWrite(lightPin1, LOW);
 //     digitalWrite(rLightPin1, LOW);
  }



  if(userInput == 'C'){
    digitalWrite(inP1A, HIGH);  
    digitalWrite(inP2A, LOW);
 //   Serial.println("DC Motor turned ON.");
  }


 if(userInput == 'D'){
    digitalWrite(inP1A, LOW);  
    digitalWrite(inP2A, LOW);
 //   Serial.println("DC Motor turned OFF.");
  }



  if(userInput == 'E'){
    servoForDoor.write(0);
  //  Serial.println("Servo is working.");
    }

  
  if(userInput == 'F'){

    servoForDoor.write(55);
  //  Serial.println("Servo is not working.");
    }

    if(userInput == 'G'){
    digitalWrite(relayPin2, HIGH);
 //     digitalWrite(rLightPin1, HIGH);
  }


  if(userInput == 'H'){
    digitalWrite(relayPin2, LOW);
 //     digitalWrite(rLightPin1, LOW);
  }

  }

