import socket
import serial
HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 2000        # Port to listen on (non-privileged ports are > 1023)
while True:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        conn, addr = s.accept()
        with conn:
            print('Connected by', addr)
            while True:
                data = conn.recv(1024)
                if data:
                    print(data.decode("utf-8"))
                    if(data.decode('utf-8')[0] == 'x'):
                        conn.sendall(b'Ending')
                        #Close the connection
                        
                        break
                    conn.sendall(data)
