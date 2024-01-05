# Written by Declan Ross
# Serial MASTER connection with Arduino
# LED Controller

#To download Serial
#https://www.instructables.com/id/How-to-Communicate-With-Arduino-From-a-Python-Scri/
#https://pyserial.readthedocs.io/en/latest/pyserial.html
import serial

#This checks if the byte recieved is correct
verificationSendCode = b'5'
verificationRecieveCode = b'8'

checkVerifOnRead = False

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
