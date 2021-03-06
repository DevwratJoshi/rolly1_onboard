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
    elif d == 'rslf':
        return "frontright\n"
    elif d == 'rbls':
        return "backright\n"
    elif d == 'rblf':
        return "hardright\n"
    elif d == 'rfls':
        return "frontleft\n"
    elif d == 'rslb':
        return "backleft\n"
    elif d == 'rflb':
        return "hardleft\n"
    else:
        return "stop\n"
ser = serial.Serial(port='/dev/ttyUSB0', baudrate=9600, timeout=1)
ser.flush()
while True:
 with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    print("Bound port")
    s.listen()
    conn, addr = s.accept()
    with conn:
        print('Connected by', addr)
        while True:
            data = conn.recv(1024)
            if data:
                data = data.decode('utf-8')

                if(data[0] == 'x'):
                    conn.sendall(b'Ending')
                    break
                else:
                    command = get_command(data) 
                    print("Got from remote : " + command)
                    
                    ser.write(command.encode('utf-8'))
                    line = ser.readline().decode('utf-8')
                    print("Got from arduino: " + line)
        print("Connection broken\n")
        sleep(1.0)
