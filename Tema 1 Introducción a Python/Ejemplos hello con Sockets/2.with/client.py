#!/usr/bin/python3

import socket

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    s.sendto("hello".encode(), ('localhost', 1234))
