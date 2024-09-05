#!/usr/bin/env python3

import sys
import socket
import sensor_pb2

# Control línea argumentos
if len(sys.argv) < 2:
    print('Usage: ./uddp-client.py <host>')
    exit()

# Socket envío del cliente - UDP
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
destination = (sys.argv[1], 2002)

# Llamada a método lectura del sensor protobuf (IMPORTANTE SABER SU PROTOCOLO)
reading = sensor_pb2.Reading()
# Definición de campos a enviar: ID, TIPO, VALOR, UNIDADES
reading.Id = 1
reading.type = sensor_pb2.Reading.HUMIDITY
reading.value = 0.2
reading.unit = "kg/m3"

# Mandamos a serializar al sensor, se imprime (b'') y envía
data = reading.SerializeToString()
print(data)
sock.sendto(data, destination)
sock.close()
