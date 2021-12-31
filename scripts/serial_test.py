#!/usr/bin/env python3
import serial
from time import sleep
HOST = '' 
PORT = 2000        # Port to listen on (non-privileged ports are > 1023)
def get_command(d):
        if d:
            return "<1.0,1.0>"
        return "<0.0,0.0>"
def main():
    ser = serial.Serial(port='/dev/ttyUSB0', baudrate=115200, timeout=1)
    ser.flush()
    data = ''
    while True: 
        command = get_command(True) 
        print(f"Command is {command}")
        ser.write(command.encode('utf-8'))
        print("Got from arduino: ")
        print(ser.readline())
        sleep(5)
        command = get_command(False) 
        print(f"Command is {command}")
        ser.write(command.encode('utf-8'))
        print("Got from arduino: ")
        print(ser.readline())
        sleep(5)
            
if __name__ == '__main__':
    main()