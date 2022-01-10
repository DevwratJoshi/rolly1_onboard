import RPi.GPIO as GPIO
import time
from threading import Thread, Lock
import math
import numpy as np

class SensorTurretHandler:
    '''
    A class that handles rolly's sensor turret
    This consists of a number of sensors mounted on a servo motor turret
    (For now, only a distance sensor)

    On instantization, this class will:
    1) Set the servo motor to the initial position 
    2) Rotate the servo turret back and forth between 0 and 180 degrees at the prescribed step resolution and freqency
    3) Take sensor readings at every step
    '''
    def __init__(self, servoPin=25, ultraTrigger=18, ultraEcho=24, scanFreq=1, scanRes=0.0174533):
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
        GPIO.setup(self.ultraTrig, GPIO.OUT)        
        GPIO.setup(self.ultraEcho, GPIO.IN)        
        self.servo = GPIO.PWM(servoPin, 50) # Creating the PWM instance
        self.servo.start(2.5) #Initialize the servo to the 0 position
        time.sleep(0.5) #Wait for the servo to get to the required position
        self.stop_requested = False
        self.thread = Thread(target=self.scanDistances, daemon=True)
        self.scan_mutex = Lock()
        self.lastDutyCycle = 0.

        self.step = (self.scanRes/math.pi) * (CONSTS.maxServoDuty - CONSTS.minServoDuty)
        # The time per step in milliseconds
        self.stepTime = (1.0/(2*scanFreq)) * (scanRes/math.pi) * 1000
        self.scan_angles = np.arange(CONSTS.minServoAngle, CONSTS.maxServoAngle, self.scanRes)
        self.totalSteps = len(self.scan_angles)
        self.dutyCycles = self.scan_angles/(CONSTS.maxServoAngle - CONSTS.minServoAngle) * (CONSTS.maxServoDuty - CONSTS.minServoDuty) + CONSTS.minServoDuty
        #print(self.dutyCycles)
        self.latestScan = np.zeros((self.totalSteps, 2)) # Distance value, degrees
        self.latestScan[:,1] = self.scan_angles
        #print(self.stepTime)
        self.reset_motor()
        
        self.thread.start()
    
    def __del__(self):
        self.stop()

    def reset_motor(self):
        self.servo.ChangeDutyCycle(CONSTS.minServoDuty)
        self.lastDutyCycle = CONSTS.minServoDuty
        time.sleep(0.5)
        return

    def measureDistance(self):
        '''
        Return distance measurement taken by the distance sensor 
        '''
            # set Trigger to HIGH
        GPIO.output(self.ultraTrig, True)
    
        # set Trigger after 0.01ms to LOW
        time.sleep(0.00001)
        GPIO.output(self.ultraTrig, False)
    
        startTime = time.time()
        stopTime = time.time()
    
        # save startTime
        while GPIO.input(self.ultraEcho) == 0:
            startTime = time.time()
        
        # save time of arrival
        while GPIO.input(self.ultraEcho) == 1:
            stopTime = time.time()
            if stopTime - startTime > 0.0176:
                return -1
        

        # multiply with the sonic speed (343 m/s)
        # and divide by 2, because there and back
        distance = ((stopTime - startTime) * 343) / 2
        #print(distance) 
        return distance
    
    def changeDutyCycle(self, value):
        '''
        Change duty cycle of the servo, and also store the last value written to the servo
        '''
        self.servo.ChangeDutyCycle(value)
        self.lastDutyCycle = value

    def scanDistances(self):
        '''
        This function is meant to be called in a separate thread. 
        It controls setting the servo duty cycle and taking the distance scans
        '''
        # The direction the motor is turning in. +1 for anti-clockwise and -1 for clockwise
        direction = 1
        nextCycle = CONSTS.minServoDuty
        scanCounter = 0
        duty_range = CONSTS.maxServoDuty - CONSTS.minServoDuty
        currentScan = np.zeros(self.latestScan.shape)
        currentScan[:,1] = self.scan_angles
        while 1:
            # Check if program is to stopped
            if(self.stop_requested):
                self.reset_motor()
                self.stop_requested = False
                return
            start_time = time.time()*1000

            currentScan[scanCounter][0] = self.measureDistance()
            scanCounter += direction
            
            if scanCounter >= self.totalSteps:
                direction = -1
                scanCounter = self.totalSteps -1
                self.scan_mutex.acquire()
                self.latestScan = np.copy(currentScan)
                self.scan_mutex.release()
                currentScan[:,0] = np.ones(self.totalSteps) * -1

            elif scanCounter < 0:
                direction = 1
                scanCounter = 0
                self.scan_mutex.acquire()
                self.latestScan = np.copy(currentScan)
                self.scan_mutex.release()
                currentScan[:,0] = np.ones(self.totalSteps) * -1
            #print(self.dutyCycles[scanCounter])       
            self.changeDutyCycle(self.dutyCycles[scanCounter])
            
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
    from constants import CONSTS
    GPIO.setmode(GPIO.BCM)
    #d=SensorTurretHandler(scanRes=0.0873)
    d=SensorTurretHandler(scanRes=0.1)

    time.sleep(2)
    while 1:
        time.sleep(2)
        #print(d.latestScan)
    
    d.stop()

else:
    from .constants import CONSTS    
