#!/usr/bin/python3

import socket
import sys
import time

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
user_address = sys.argv[1]
port = sys.argv[2]
user = (user_address, int(port))
sock.bind(user)

sock.listen(1)

while True:
    print('Waiting for a connection from the server .... ')
    connection, server_address = sock.accept()

    try:
        print('Connection from {}'.format(server_address))

        # Receive the data in small chunks and retransmit it
        while True:
            data = connection.recv(25)
            print('Received data: {}'.format(data))
            if data == 'STOP':
                print('No more data from {}'.format(server_address))
                connection.sendall('Acknowledgement from user')
                break

    finally:
        # Clean up the connection
        connection.close()