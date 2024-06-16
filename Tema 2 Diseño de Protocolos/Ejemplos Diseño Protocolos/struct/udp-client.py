#!/usr/bin/python3

import sys
import socket
import struct

# Constantes de tipo de sensor
UNKNOWN = 0
HUMIDITY = 1
PRESSURE = 2
ACCELERATION = 3


def serialize_reading(id_, type_, value, unit):
    '''Serializar 16 bits, Byte sin signo, float, Bytes sin signo (constante de arriba),
    string de cadena con longitud = unit (puesto con {})'''
    unit = unit.encode()
    unit_len = len(unit)
    return struct.pack('!hBfB{}s'.format(unit_len), id_, type_, value, unit_len, unit)

# Si no hay 1 argumento (+ nombre del programa) = error
if len(sys.argv) != 2:
    print(__doc__.format(__file__))
    sys.exit(1)

# Enviar dato serializado a la ip del argumento
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
data = serialize_reading(id_=8, type_=PRESSURE, value=16.3, unit='bar')
print(data)
sock.sendto(data, (sys.argv[1], 2000))
sock.close()