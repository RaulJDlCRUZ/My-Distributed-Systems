#!/usr/bin/python3

import socket

s =  socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.sendto("hello".encode(), ('localhost', 1234))
s.close()
