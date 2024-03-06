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
 //     Serial.println("LED turned ON.");
  }


  if(userInput == 'B'){
    digitalWrite(lightPin1, LOW);
 //     Serial.println("LED turned OFF.");
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
  //  Serial.println("Door is opened using Servo motor).");
    }

  
  if(userInput == 'F'){

    servoForDoor.write(55);
  //  Serial.println("Door is closed using Servo motor.");
    }

    if(userInput == 'G'){
    digitalWrite(relayPin2, HIGH);
 //     Serial.println("Light is turned ON.");
  }


  if(userInput == 'H'){
    digitalWrite(relayPin2, LOW);
 //     Serial.println("Light is turned OFF.");
  }

  if(userInput == 'I'){
    digitalWrite(lightPin1, HIGH);
    digitalWrite(inP1A, HIGH);  
    digitalWrite(inP2A, LOW);
    servoForDoor.write(0);
    digitalWrite(relayPin2, HIGH);
 //     Serial.println("Everything is turned ON.");
  }

  if(userInput == 'J'){
    digitalWrite(lightPin1, LOW);
    digitalWrite(inP1A, LOW);  
    digitalWrite(inP2A, LOW);
    servoForDoor.write(55);
    digitalWrite(relayPin2, LOW);

 //     Serial.println("Everything is turned OFF.");
  }

  }

