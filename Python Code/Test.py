import mouse

import Arduino
import time
import serial
from tkinter import *
ser1 = serial.Serial("COM3", 115200, timeout=0.05)

def requestAll():
    stringVal = Arduino.communicate(ser1, True, 'A', 0)
    print(stringVal)
    return


while(1):
    requestAll()