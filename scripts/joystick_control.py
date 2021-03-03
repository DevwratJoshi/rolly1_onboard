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
                            #Close the connection
                            break
                        else:
                            command = get_command(data) 
                            print(command)
                            ser.write(command.encode('utf-8'))
                            print(ser.readline())
                print("Connection broken\n")
                sleep(1.0)
