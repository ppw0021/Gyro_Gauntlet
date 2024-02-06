/*
   Written by Declan Ross
   01/09/2020
   Wireless mouse transmitter
*/
/*
int LEFTMOUSE = 5;
int RIGHTMOUSE = 4;
int CALIBRATE = 2;
*/
//Include Libraries
#include <SPI.h>
#include <nRF24L01.h>
#include <RF24.h>
#include <Wire.h>
#include <MPU6050.h>

MPU6050 mpu;

// Pitch, Roll and Yaw values
float pitch = 0;
float roll = 0;
float yaw = 0;
float timeStep = 0.01;


//Codes used to verify to the python script that the data entry code was recieved correctly
char pythonSendVerifCode = '5';
char pythonReadVerifCode = '8';

int LeftMouseClick = 5;
String LeftMouseState = "f";

int CenterButton = 2;
String CenterButtonState = "f";

int RightMouseClick = 4;
String RightMouseState = "f";

//create an RF24 object
RF24 radio(9, 8);  // CE, CSN

//address through which two modules communicate.
const byte address[6] = "00001";

const bool TEST = false;

void setup() {
  //Button state declaration
  pinMode(LeftMouseClick, INPUT);
  pinMode(CenterButton, INPUT);
  pinMode(RightMouseClick, INPUT);

  while (!mpu.begin(MPU6050_SCALE_2000DPS, MPU6050_RANGE_2G)) {
    //Serial.println("Could not find a valid MPU6050 sensor, check wiring!");
    delay(500);
  }

  // Calibrate gyroscope. The calibration must be at rest.
  // If you don't want calibrate, comment this line.
  mpu.calibrateGyro();

  // Set threshold sensivty. Default 3.
  // If you don't want use threshold, comment this line or set 0.
  mpu.setThreshold(3);

  if (TEST) {
    Serial.begin(115200);
  }
  radio.begin();
  //set the address
  radio.openWritingPipe(address);
  //Set module as transmitter
  radio.stopListening();
  radio.setRetries(0, 0);
}

void loop() {
  unsigned long currentTime = millis();
  static unsigned long previousTime = 0;
  static unsigned long interval = 1;
  while (currentTime - previousTime >= interval) {
    previousTime = currentTime;
  }

  // Read normalized values
  Vector norm = mpu.readNormalizeGyro();
  // Calculate Pitch, Roll and Yaw
  pitch = pitch + norm.YAxis * timeStep;
  roll = roll + norm.XAxis * timeStep;
  yaw = yaw + norm.ZAxis * timeStep;
  
  //Send message to receiver

  String dataType = "A";
  String yawVal = String(yaw);
  String pitchVal = String(pitch);
  String rollVal = String(roll);
  if (digitalRead(LeftMouseClick) == HIGH) {
    LeftMouseState = "t";
  } else {
    LeftMouseState = "f";
  }
  if (digitalRead(CenterButton) == HIGH) {
    CenterButtonState = "t";
  } else {
    CenterButtonState = "f";
  }
  if (digitalRead(RightMouseClick) == HIGH) {
    RightMouseState = "t";
  } else {
    RightMouseState = "f";
  }
  //String dataToWrite = "A:0.00:0.00:T:T";
  String dataToWrite = String(dataType + ":" + rollVal + ":" + yawVal + ":" + LeftMouseState + ":" + RightMouseState + ":" + CenterButtonState + ":" + pitchVal + ":" + "0");
  int dataLength = dataToWrite.length();
  char i[dataLength];

  dataToWrite.toCharArray(i, dataLength);

  radio.write(&i, sizeof(i));
  if (TEST) {
    Serial.println(i);
  }
}
