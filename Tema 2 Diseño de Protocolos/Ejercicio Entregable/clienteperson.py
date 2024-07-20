#!/usr/bin/python3

# AUTOR = RAÚL JIMÉNEZ DE LA CRUZ

import sys
import socket
from person_pb2 import Person, Result

PORT = 4080

if len(sys.argv) < 2:
    print('Usage: ./clienteperson.py <host>')
    exit(-1)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
destination = (sys.argv[1], PORT)

person = Person()

person.name = 'Raúl Jiménez de la Cruz'
person.dni = 2319161
person.email.extend(['Raul.Jimenez', 'alu', 'uclm', 'es'])

data = person.SerializeToString()
sock.sendto(data, destination)

response_data = sock.recv(1024)
_response = Result()
_response.ParseFromString(response_data)
print(_response)