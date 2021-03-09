#This program takes motor pwm values from the user to allow setting pwm values randomly
# This is to collect data to get a conversion function between velocity values and pwm
import serial
from time import sleep

class Values:
    def __init__(self):
        self.r_pwm = 0
        self.l_pwm = 0
        self.pause = False #If this is true, do not write anything to serial
        self.linear_mode = True #If this is true, both values have the same sign
                           #Else have opposite signs
    def set_r_pwm(self, val):
        self.r_pwm = val
    
    def set_l_pwm(self, val):
        self.l_pwm = val
    
    def get_pwm_command(self):
        if not self.pause:
            if self.linear_mode:
                return str(self.r_pwm) + ":" + str(self.l_pwm)
            else:
                return str(self.r_pwm) + ":" + str(-self.l_pwm)
        else:
            return '0:0'

if __name__ == '__main__':
    ser = serial.Serial(port='/dev/ttyACM0', baudrate=9600, timeout=1)
    ser.flush() 
    v = Values()
    i = ''

    while True:
        print("Enter i to increase pwm by 10 each")
        print("Enter d to decrease pwm by 10 each")
        print("Enter r to reset pwm to 0")
        print("Enter t to toggle between linear and rotational motion")
        print("Enter p to pause/play")
        print("Enter x to exit")
        i = input()
        if i == 'i':
            v.set_l_pwm((v.l_pwm+10)%255)
            v.set_r_pwm((v.r_pwm+10)%255)
            
        elif i == 'd':
            v.set_l_pwm((v.l_pwm-10)%255)
            v.set_r_pwm((v.r_pwm-10)%255)
        
        elif i == 'r':
            v.set_l_pwm(0)
            v.set_r_pwm(0)

        elif i == 't':
            v.linear_mode = not v.linear_mode   

        elif i == 'p':
            v.pause = not v.pause        

        elif i == 'x':
            v.set_r_pwm(self, 0)
            v.set_r_pwm(self, 0)
            ser.write(v.get_pwm_command().encode('utf-8'))
            line = ser.readline().decode('utf-8')
            print("Got from arduino: " + line)
            print("\n Goodbye")
            break
        
        elif i =='':
            pass 
        
        print("Current status: \n")
        print(("Linear " if v.linear_mode else "Rotational ") + "mode\n")
        print(("Paused " if v.pause else "Active") + "\n")
        print("Right pwm = " + str(v.r_pwm) + "  Left pwm = " + str(v.l_pwm))

        ser.write((v.get_pwm_command() + "\n").encode('utf-8'))
        line = ser.readline().decode('utf-8')
        print("Got from arduino: " + line)