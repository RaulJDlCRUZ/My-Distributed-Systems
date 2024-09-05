#!/usr/bin/python3

import socket

# s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # familia ip de tipo udp
# s.bind(('localhost', 8808))  # tupla ip-puerto

# msg, addr = s.recvfrom(1024)  # tamanyo buffer de entrada

# s.close()

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    s.bind(('localhost', 8808))  # tupla ip-puerto
    msg, addr = s.recvfrom(1024)  # tamanyo buffer de entrada
    
print(msg.decode())