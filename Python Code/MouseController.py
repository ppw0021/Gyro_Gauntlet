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
HeightSens = 8
LengthSens = 8
scrollSens = 0.2

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

ser1 = serial.Serial("COM8", 115200, timeout=0.05)
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
    except:
        print("hiccuip")