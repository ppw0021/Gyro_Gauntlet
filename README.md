# Gyro Mouse

This is an Arduino powered device that wireless connects to a computer via a RF module. You can control the computer as if you had an invisible mouse in your hand using hand gestures and motions.

![IMG_6590 (1)](https://github.com/ppw0021/gyro_gauntlet/assets/143673072/96c9b333-1e1e-452d-898b-adc47e2145eb)

## Description

The Gyro Mouse is a wrist mounted arduino-powered device that uses RF modules to communicate with another arduino and interpreted and translated into mouse movements using a Python script.
Standard gestures:
- By clicking your left finger, you left click.
- By clicking your middle finger you right click.
- By clicking your ring finger, you re-centre the mouse.
- When clicking left and right at the same time, the mouse is locked in place, and any movements made by the mouse are translated into scrolling motion instead of mouse movements.


## 3D printed parts and CNC machined parts
The frame of the gyro mouse is 3D printed and modeled to fit onto the right hand of an individual. The finger rings are also 3D printed and bend slightly to allow for clicking gestures.

Frame:

![RenderedFrame](https://github.com/ppw0021/gyro_gauntlet/assets/143673072/8538975c-7ad5-48af-9a76-9b9e0a74214e)

I designed the frame using Fusion 360.
I recommend using Black, White and Clear PLA or ABS plastic at 0.1mm layer height for best results. 

The PCB board was designed using DipTrace and machined using a CNC machine.

![IMG_5210](https://github.com/ppw0021/gyro_gauntlet/assets/143673072/83cb326c-9281-4c9c-afaf-0eb1988d2b3c)

Based on this schematic I created:

![image](https://github.com/ppw0021/gyro_gauntlet/assets/143673072/5cd9cf24-aa88-410b-8ee5-63db371bbb70)

Drilled PCB:

![IMG_5208](https://github.com/ppw0021/gyro_gauntlet/assets/143673072/5a4f467c-fdcc-4e9d-9ed2-c3f59787c7bd)


## Electronics

This project has 2 seperate microcontrollers. One that connects to the computer and one that is on board the gyro-glove itself. 
Gyro-Glove components:
- 3x button switches
- 1x Arduino Nano
- 1x MPU6050 gyroscope module
- 3x 1k ohm resistors (pulldown)
- 1x 9V battery and battery holder
- 1x power switch
- 1x NRF24L01 Radio module

Receiver module components
- 1x Arduino uno
- 1x NRF24L01 Radio module

## Prerequisites

The following libraries are required:
pip install mouse
pip install pyserial 
or 
pip3 install mouse
pip install pyserial
pip install tkinter


## Code

There is three programs that are needed for the Gyro-Gauntlet to work. The first program (transmitter.ino) is loaded onto the Arduino Nano onboard the gyro-glove, this code translates the readings from the Gyroscope module into numbers (as well as the states of the switches) and transmits it to the reciever module which has the second program loaded (reciever.ino). This code processes the recieved transmission and transmitts it via serial to the third and final code, the python script (MouseController.py) that inteprets the numbers and states of the switches and converts the raw rotation numbers and switch positions into moues movements. There is also an additional file named Arduino.py that acts as a function library for MouseController.py.

transmitter.ino
```cpp
/*
   Written by Declan Ross
   Wireless mouse transmitter
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


```

reciever.ino
```cpp
//Include Libraries
#include <SPI.h>
#include <RF24.h>

//create an RF24 object
RF24 radio(9, 8);  // CE, CSN

//address through which two modules communicate.
const byte address[6] = "00001";

char text[32] = {0};

char pythonSendVerifCode = '5';
char pythonReadVerifCode = '8';

bool TEST = false;

void setup()
{
  while (!Serial);
  Serial.begin(115200);

  radio.begin();

  //set the address
  radio.openReadingPipe(0, address);

  //Set module as receiver
  radio.startListening();
}

void loop()
{
  //Read the data if available in buffer
  if (radio.available())
  {
    //Serial.println("Read");
    radio.read(&text, sizeof(text));
    
  }
  if (TEST)
    {
      String dataToWrite = text;
      Serial.print(dataToWrite);
      Serial.write("\n");
    }
  if (Serial.available() > 0)
  {
    //Store the read data as a CHAR, this is an indicator to what the controller wants (Lowercase means UPDATE FROM python, uppercase means to UPDATE python)
    char dataRecieved = Serial.read();
    //Example of UPDATE FROM python if statement
    if (dataRecieved == 'r')
    {
      //Handshake byte to confirm arduino is ready to recieve
      Serial.write(pythonSendVerifCode);
      //Wait until python sends back a value
      while (!Serial.available()) {}
      //Read the value
      char Val = Serial.read();
      //Update the independent function
    }

    if (dataRecieved == 'I') {
      Serial.write(pythonReadVerifCode);
      Serial.write("1\n");
      TEST = true;
    }
    if (dataRecieved == 'A') {
      String dataToWrite = text;
      Serial.print(dataToWrite);
      Serial.write("\n");
    }
    else {}
  }
  unsigned long currentTime = millis();
  static unsigned long previousTime = 0;
  static unsigned long interval = 1;
  while (currentTime - previousTime >= interval) {
    previousTime = currentTime;
  }
}

```

Arduino.py
```python
# Written by Declan Ross
# Serial MASTER connection with Arduino

#To download Serial
#https://www.instructables.com/id/How-to-Communicate-With-Arduino-From-a-Python-Scri/
#https://pyserial.readthedocs.io/en/latest/pyserial.html
import serial

#This checks if the byte recieved is correct
verificationSendCode = b'5'
verificationRecieveCode = b'8'

checkVerifOnRead = False

def getPos(serialData):
    return serialData.readline();

def communicate(serialData, requesting, data, val):
    if (requesting == False):
        serialData.write(data.encode())
        checkVerification = serialData.read()
        if (checkVerification != verificationSendCode):
            print("Arduino Handshake failed")
            return
        else:
            print("Arduino Handshake succeeded")
            serialData.write(chr(val).encode())
            #Value as char
            #print(chr(val))
            return
    if (requesting == True):
        serialData.write(data.encode())
        if checkVerifOnRead == True:
            checkVerification = serialData.read()
            if (checkVerification != verificationRecieveCode):
                print("Arduino Handshake failed")
                return
            else:
                print("Arduino Handshake succeeded")
                rawData = serialData.readline()
                return rawData
        else:
            rawData = serialData.readline()
            return rawData            
        
        
def connect(serialData, data, val):
    if (1 == 1):
        serialData.write(data.encode())
        checkVerification = serialData.read()
        if (checkVerification != verificationRecieveCode):
            return
        else:
            print("Arduino Handshake succeeded")
            rawData = serialData.readline()
            if (float(rawData) == 1.0):
                return True
            else:
                return False
#def sendRequest(variableData, data):
    #variableData.write(data.encode())
    #x=variableData.readline()
    #y=variableData.readline()
    #z=variableData.readline()
    #print(x, y, z)   
    #return

#Arduino value is not being flushed correctly :///
#def sendShutDown(variableData):
    #variableData.write('y'.encode())
    #print(variableData.readline())
    #return

```

MouseController.py
```
#pip install mouse
#pip install pyserial
#or pip3 install mouse
import mouse

import Arduino
import time
import serial
from tkinter import *

#Resolution
ScreenHeight = 1440
ScreenLength = 2560

#Screen center
HeightStartPos = (ScreenHeight/2)
LengthStartPos = (ScreenLength/2)

#Sensitivity
HeightSens = 16
LengthSens = 16
scrollSens = 0.5

#Offset from center for calibration
HeightOffset = 0
LengthOffset = 0

leftHeldDown = False
rightHeldDown = False

moveMouse = True
mouseScrolling = False

currentTime = 0

last = 0
startTime = time.time()

ser1 = serial.Serial("COM3", 115200, timeout=0.05)
def tryConnect():
    data = 'I'
    return Arduino.connect(ser1, data, 0)

def requestGyroPos(data):
    stringVal = Arduino.communicate(ser1, True, data, 0)
    return (stringVal.decode("utf-8")).strip()

def requestAll():
    #stringVal = Arduino.communicate(ser1, True, 'A', 0)

    stringVal = Arduino.getPos(ser1);
    print(stringVal)
    stringVal = stringVal.decode("utf-8")
    X = stringVal.split(":")
    return X

for x in range(300):
    connectionEstablished = False
    print("Connecting...")
    if connectionEstablished == False:
        y = tryConnect()
    if (y == True):
        connectionEstablished = True
        print("Connection established")
        break
    if (x == 299) and (connectionEstablished == False):
        print("Connection failed")
        

while(True):
    #Use for 60HZ
    #time.sleep(0.010);
    #time.sleep(0.016)
    #Use for 144HZ
    #time.sleep(0.00694)
    try:
        AllDataList = requestAll()
    except:
        continue
    #print(AllDataList)
    if (AllDataList[0] == "A"):
	#x = float(AllDataList[1].strip())
        #y = float(AllDataList[2].strip())

	#Reversed
        y = 0 - float(AllDataList[1].strip())
        x = float(AllDataList[2].strip())
        subfinalx = LengthStartPos - ((LengthSens * x) - LengthOffset)
        subfinaly = HeightStartPos - ((HeightSens * y) - HeightOffset)
        finalx = float(subfinalx)
        finaly = float(subfinaly)
        #print((finalx, finaly))
        if (AllDataList[3] == 't'):
            if mouseScrolling == False:
                if leftHeldDown == False:
                    mouse.press(button='left')	
                    leftHeldDown = True            
            if (AllDataList[4] == 't'):
                mouseScrolling = True
                moveMouse = False
                if (currentTime == 0):
                    currentTime = time.time()
                val = time.time() - currentTime
                if (val) > 0.00694:
                    currentTime = time.time()
                    difference = subfinalx - last
                    moveAmount = (difference * scrollSens)/-5
                    mouse.wheel(delta=(moveAmount))
                    last = finalx
                mouse.release(button="left")

             
        if (AllDataList[5] == 't'):
            LengthOffset = (LengthSens * x)
            HeightOffset = (HeightSens * y)
        if (AllDataList[4] == 't'):
            if (rightHeldDown == False):
                if (mouseScrolling == False):
                    moveMouse = True
                    mouse.click(button='right')
                    rightHeldDown = True
        if (AllDataList[3] == 'f'):
            if mouseScrolling == False:
                moveMouse = True
                mouse.release(button='left')
                leftHeldDown = False           
        else:
            mouseScrolling = False	
            rightHeldDown = False 
        if (moveMouse == True):
            mouse.move(finalx, finaly, absolute=True, duration=0)

```

## Version History

* 1.0
    * Initial Release
