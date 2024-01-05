# Written by Declan Ross
# Serial MASTER connection with Arduino
# Serial Connectivity

import Arduino
import serial
from tkinter import *



#ser1 = serial.Serial('COM4', 115200, timeout=0.05)

#Guideline for Arduino.communicate;
#                                                       (Use capital letter for requesting)        (If sending)
#                    /--Serial Port  /--Requesting?  /--Code to be sent to arduino              /--Data to be sent
#Arduino.communicate(ser1,           False,          data,                                      0)

def defineSerialPort():
    global ser1 
    connectionEstablished = False
    try:
        ser1 = serial.Serial(str(comEntry.get()), 115200, timeout=0.1)
        comButton.configure(state=DISABLED)
        errorLabel.configure(text="Connecting..")
        for x in range(300):
            if connectionEstablished == False:
                y = tryConnect()
            if (y == True):
                connectionEstablished = True
                errorLabel.configure(text="Connected")
                print("Connection established")
                break
            if (x == 299) and (connectionEstablished == False):
                errorLabel.configure(text="Failed")
                comButton.configure(state=NORMAL)
                print("Connection failed")
        #errorLabel.configure(text="")
        comButton.configure(state=DISABLED)
        comEntry.configure(state=DISABLED)
        return
    except:
        comButton.configure(state=NORMAL)
        errorLabel.configure(text="False COM port")
        return
    return

def tryConnect():
    data = 'I'
    return Arduino.connect(ser1, data, 0)

def request():
    data = 'P'
    print(Arduino.communicate(ser1, True, data, 0))
    return

def beginStream():
    return

root = Tk()
root.title("LED Controller")
#Header
Label(root, text="LED Arduino Controller", font="Arial 16 bold").grid(row=0, columnspan=2)

#Labels
Label(root, text="COM Port: ").grid(row=1, column=0)
errorLabel = Label(root, text=" ", fg="red")

#Entry box
comEntry = Entry(root, state=NORMAL)
comButton = Button(root, text="Confirm", command=defineSerialPort, state=NORMAL)

reqButt = Button(root, text="Request", command=request)
reqButt.grid(row=3, columnspan=2)
begin = Button(root, text="Begin stream", command=beginStream)
begin.grid(row=4, columnspan=2)

#Grid declaration
comEntry.grid(row=1, column=1)
comButton.grid(row=2, column=1)
errorLabel.grid(row=2, columnspan=2, sticky=W)

root.mainloop()
