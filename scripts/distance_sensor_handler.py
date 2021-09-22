import RPi.GPIO as GPIO
import time
from threading import Thread, Lock
import math
import numpy as np
class DistanceSensorHandler:
    '''
    A class that handles the rolly distance sensors
    These sensors consist of a HCSR04 ultrasound sensor mounted on a SG90 servo motor
    '''
    def __init__(self, servoPin=25, ultraTrigger=18, ultraEcho=24, scanFreq=1.0, scanRes=0.0174533):
        '''
        @param servoPin The servo input pin (GPIO pin number)
        @param ultraTrigger The HCSR04 trigger pin (GPIO pin number)
        @param ultraEcho The HCSR04 echo pin (GPIO pin number)
        @param scanFreq The frequency of the rotation of the motor in rps
        @param scanRes The seperations between servo angles at which distances are measured in radian
        '''
        self.ultraTrig = ultraTrigger
        self.ultraEcho = ultraEcho
        self.scanFreq = scanFreq
        self.scanRes = scanRes
        self.thread = Thread() #Thread to handle the servo motor
        # GPIO.setmode(GPIO.BOARD)
        GPIO.setup(servoPin, GPIO.OUT)        
        self.servo = GPIO.PWM(servoPin, 50) # Creating the PWM instance
        self.servo.start(2.5) #Initialize the servo to the 0 position
        time.sleep(0.5) #Wait for the servo to get to the required position
        self.stop_requested = False
        self.thread = Thread(target=self.scanDistances)
        self.thread.start()
        self.lastDutyCycle = 0.
        self.step = (self.scanRes/math.pi) * (5)
        # The time per step in milliseconds
        self.stepTime = (1.0/(2*scanFreq)) * (scanRes/math.pi) * 1000
    def reset_motor(self):
        self.servo.ChangeDutyCycle(2.5)
        self.lastDutyCycle = 5.
        time.sleep(0.5)
        return
    def __del__(self):
        self.stop()

    def measureDistance(self):
        time.sleep(0.01)

    def scanDistances(self):
        '''
        This function is meant to be called in a separate thread. 
        It controls setting the servo duty cycle and taking the distance scans
        '''
        # The direction the motor is turning in. +1 for anti-clockwise and -1 for clockwise
        direction = 1
        nextCycle = 5
        while 1:
            # Check if program is to stopped
            if(self.stop_requested):
                self.reset_motor()
                self.stop_requested = False
                return
            self.servo.ChangeDutyCycle(nextCycle)
            start_time = time.time()*1000
            self.lastDutyCycle = nextCycle

            # TODO: Get distance data scan point here
            self.measureDistance()

            nextCycle = self.lastDutyCycle + direction*self.step
            
            if nextCycle > 12.5:
                direction = -1
                nextCycle = 12.5

            elif nextCycle < 2.5:
                direction = 1
                nextcycle = 2.5
            
            # Wait the appropriate amount of time before the next loop cycle
            curr_time = time.time() * 1000
            # Rather than wait a set amount of time, we wait till the time taken by this step is equal to or greater than the time per step
            while curr_time - start_time < self.stepTime:
                time.sleep(0.0005) #The likely time per step is about 0.003 seconds for a 1 rps rotation freq
                curr_time = time.time()*1000
                
    def stop(self):
        if self.thread.is_alive():
            self.stop_requested = True
            self.thread.join()


if __name__ == '__main__':
    GPIO.setmode(GPIO.BCM)
    d=DistanceSensorHandler()