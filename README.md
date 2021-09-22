### Project rolly1 robot onboard code repo  

#### Objective  
This code is meant to run on board the control board on the robot. This code should be included as a submodule for the rolly1 central repo and cloned into the computer on board the robot. 

##### Arduino pinout  
|Pin | Connection | 
|:--:| :---------: |
|3| Left wheel pwm |
|5| Left wheel direction in3|
|6| Left wheel direction in4|
|9| Right wheel pwm |
|8| Right wheel direction in1|
|7| Right wheel direction in2|
|10| Left ultrasonic sensor motor control |
|11| Right ultrasonic sensor motor control |
|12| Left ultrasonic sensor trigger |
|13| Left ultrasonic sensor data |
|A0| Right ultrasonic sensor trigger |
|A1| Right ultrasonic sensor data |  

Pin 2 is saved for a  potential future external interrupt 


#### Raspberry pi 3B+ pinout
|Pin number|GPIO number|Connectiion|
|:---:|:---:|:---|
|12|25|Ultrasonic sensor trigger|
|18|24|Ultrasonic sensor echo|
|22|25|Ultrasonic sensor servo input|

The one of the raspberry pi serial port is connected to the arduino pro mini by a usb cable through an FTDI chip 