import socket
import serial
from time import sleep
HOST = '' 
PORT = 2000        # Port to listen on (non-privileged ports are > 1023)
def get_command(d):
    if d == 'rflf':
        return "forward\n"
    elif d == 'rblb':
        return "backward\n"
    else:
        return "stop\n"
def main():
    ser = serial.Serial(port='/dev/ttyUSB0', baudrate=9600, timeout=1)
    ser.flush()
    data = 'rff'
    while True: 
        command = get_command(data) 
        ser.write(command.encode('utf-8'))
        print(ser.readline())
            
if __name__ == '__main__':
    main()