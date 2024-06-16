#!/usr/bin/python3

import socket

# s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# s.sendto(b"Hola", ("localhost", 8808))
# s.close()

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    s.sendto(b"Hola", ("localhost", 8808))