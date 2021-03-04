import socket
import serial
from time import sleep
HOST = '' 
PORT = 2000        # Port to listen on (non-privileged ports are > 1023)
def get_command(d):
    if d == 'rflf':
        return "forward"
    elif d == 'rblb':
        return "backward"
    else:
        return "stop"
with serial.Serial(port='/dev/ttyUSB0', baudrate=9600) as ser:
    data = 'rff'
    command = get_command(data) 
    ser.write(command.encode('utf-8'))
    print(ser.readline())
