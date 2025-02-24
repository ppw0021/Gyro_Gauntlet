//Include Libraries
#include <SPI.h>
//#include <nRF24L01.h>
#include <RF24.h>

//create an RF24 object
RF24 radio(5, 6);  // CE, CSN

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
