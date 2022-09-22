#!/usr/bin/env python3
from calendar import TUESDAY
import socket, sys
import time
from multiprocessing import Process

#define address & buffer size
HOST = ""
PORT = 8001
BUFFER_SIZE = 1024

#create a tcp socket
def create_tcp_socket():
    print('Creating socket')
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except (socket.error, msg):
        print(f'Failed to create socket. Error code: {str(msg[0])} , Error message : {msg[1]}')
        sys.exit()
    print('Socket created successfully')
    return s

    
#get host information
def get_remote_ip(host):
    print(f'Getting IP for {host}')
    try:
        remote_ip = socket.gethostbyname( host )
    except socket.gaierror:
        print ('Hostname could not be resolved. Exiting')
        sys.exit()

    print (f'Ip address of {host} is {remote_ip}')
    return remote_ip

#send data to server
def send_data(serversocket, payload):
    print("Sending payload")    
    try:
        serversocket.sendall(payload)
    except socket.error:
        print ('Send failed')
        sys.exit()
    print("Payload sent successfully")

def handle_echo(proxy_end, addr, conn):
    #recieve data, and send it to proxy_end
    payload = conn.recv(BUFFER_SIZE)

    #send the data and shutdown
    send_data(proxy_end, payload)
    proxy_end.shutdown(socket.SHUT_WR)

    #continue accepting data until no more left
    full_data = b""
    while True:
        data = proxy_end.recv(BUFFER_SIZE)
        if not data:
            break
        full_data += data
    conn.sendall(full_data)

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    
        #QUESTION 3
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        #bind socket to address
        s.bind((HOST, PORT))
        #set to listening mode
        s.listen(2)
        
        #continuously listen for connections
        while True:
            conn, addr = s.accept()
            print("Connected by", addr)
            
            with create_tcp_socket() as s_google:
                #act as a client and connect to google
                host = 'google.com'
                port = 80
                #make the socket, get the ip, and connect
                remote_ip = get_remote_ip(host)
                s_google.connect((remote_ip , port))

                p = Process(target=handle_echo, args=(s_google, addr, conn))
                p.daemon = True
                p.start()

            conn.close()

if __name__ == "__main__":
    main()
