#!/usr/bin/python3

import socket
import sys
from time import sleep
import random
import time
import string
from datetime import datetime
import multiprocessing

no_of_users = int(sys.argv[1])
no_of_waus = 1

# Create sockets for WAUs
socket_WAUs = []
for i in range(no_of_waus):
    socket_WAUs.append(socket.socket(socket.AF_INET, socket.SOCK_DGRAM))

# Create sockets for users
socket_users = []
for j in range(no_of_users):
    socket_users.append(socket.socket(socket.AF_INET, socket.SOCK_DGRAM))

# Create ports for WAUs
ports_WAUs = []
first_port = 10000
for k in range(no_of_waus):
    port_k = ('10.10.0.10', first_port + k)
    ports_WAUs.append(port_k)

# Binding ports to sockets for WAUs
print('Socket creation at server side for WAUs')
for i in range(no_of_waus):
    sock_i = socket_WAUs[i]
    port_i = ports_WAUs[i]
    print('Starting on %s port %s '% port_i)
    sock_i.bind(port_i)

# Create ports for users
ports_users = []
for l in range(no_of_users):
    port_l = ('10.10.0.10', first_port + no_of_waus + l)
    ports_users.append(port_l)

# Binding ports to sockets for users
print('Socket creation at server side for users')
for i in range(no_of_users):
    sock_i = socket_users[i]
    port_i = ports_users[i]
    print('Starting on %s port %s '% port_i)
    sock_i.bind(port_i)

# We have now created ports at the server side for all WAUs and users


def send_message(socket_i, message, i):
    UDP_IP = '10.10.' + sys.argv[i + 2]
    UDP_PORT = first_port + i
    socket_i.sendto(message, (UDP_IP, UDP_PORT))
    print('STOP sent to AP at {}'.format(UDP_IP, UDP_PORT))


def rx_message(socket_i):
    socket_i.recv(50)
    print('Received frequency offset from user!')


def listen_and_accept(socket_i):
    socket_i.listen(1)
    while True:
        connection, remote_address = socket_i.accept()
        print('Connection accepted from {}'.format(remote_address))


try:
    d_list = []

    for i in range(len(socket_users)):
        sock_i = socket_users[i]
        d = multiprocessing.Process(name='Rx from users', target=rx_message, args=(sock_i,))
        d.start()
        d_list.append(d)

    for d in d_list:
        d.join()

    print('All users have estimated their respective frequency offsets! Stopping transmissions from AP now')

    message = 'STOP'
    print('AP will stop sending training symbols now ... ')
    d_list = []
    for i in range(len(socket_WAUs)):
        sock_i = socket_WAUs[i]
        d = multiprocessing.Process(name='Sending to WAUs', target=send_message, args=(sock_i, message, i))
        d.start()
        d_list.append(d)

    for d in d_list:
        d.join()

finally:
    print('Closing all the sockets')
    for i in range(len(socket_WAUs)):
        sock_i = socket_WAUs[i]
        sock_i.close()
    for i in range(len(socket_users)):
        sock_i = socket_users[i]
        sock_i.close()
