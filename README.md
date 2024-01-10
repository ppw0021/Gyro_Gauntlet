# Gyro Mouse

This is an Arduino powered device that wireless connects to a computer via a RF module. You can control the computer as if you had an invisible mouse in your hand using hand gestures and motions.

![IMG_5898](https://github.com/ppw0021/gyro_gauntlet/assets/143673072/e1c3b3ce-2eb7-459b-b04b-eb336367a3fa)

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



## Electronics

The microcontroller for this project is an Arduino Nano with an ATmega328p chip onboard.
The following components are required for each laser gun:
- 1x IR LED  (For signal transmission)
- 1x 31MM biconvex lens 27MM focal point  (For straightening the IR light from the IR LED)
- 6x IR Receiver TSOP4838 DIP3  (For receiving transmissions from other laser guns)
- 1x i2c 16x2 LCD display modules  (For displaying UI to user)
- 1x YX5300 UART Serial MP3 player  (For playing sounds)
- 1x MicroSD card  (For storing sounds)
- 3x DC3v Button Vibrating Motors  (For providing haptic feedback)
- 6x push buttons  (For navigating UI and reload switches)
- 1x PAM8403 digital amplifier (For amplifying the audio signal from the MP3 Player)
  - 1x 4omh speaker
  - 1x 4.7uF capacitor
  - (Please note these parts are quite arbitrary and were subject is guesswork, results may vary)
- 7x 1k ohm resistors (Various pulldown )
- 1x NPN transistor
- 

## Code

The code is very straight forward and simple, but a calibration will need to be done to find the correct threshold.
```
CODE HERE
```

## Version History

* 1.0
    * Initial Release
