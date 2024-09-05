#!/usr/bin/python3 -u
# AUTOR = RAÚL JIMÉNEZ DE LA CRUZ 
"Usage: {0} <host> <port>"
import sys
import socket
import struct

# 192.168.8.224 : 4080
# GL-ITA-56   // inf-ta-net

server_addr = (sys.argv[1], int(sys.argv[2]))


def deserialize_reading(data):
    # FIXME: complete this function for data unmarshalling
    # PASO 1: LONGITUD DE LA CADENA DEL COLOR
    len_received, = struct.unpack('!f', data[:4])
    len_received = int(len_received) # lo convierto a entero para concretar longitud en formato cadena
    # PASO 2: EXTRAER CADENA
    color, = struct.unpack(f'!{str(len_received)}s', data[4:4+len_received])
    # PASO 3: EXTRAER HORA EXACTA
    hour, minute, second, = struct.unpack('!ilh', data[4+len_received:4+len_received+struct.calcsize('ilh')])
    # DEVOLVER DATOS
    return color, hour, minute, second


if len(sys.argv) != 3:
    print(__doc__.format(__file__))
    sys.exit(1)

# FIXME: write your own UCLM ID
uclm_id = 'Raul.Jimenez'  # if your email is John.Doe@alu.uclm.es

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

print('Sending UCLM ID...')
msg = 'UID'.encode() + uclm_id.encode()
sock.sendto(msg, server_addr)

msg = sock.recv(1024)
reading = deserialize_reading(msg)
sending_str = 'RES' + reading[0].decode() + ' ' + str(reading[1]) +':'+ str(reading[2]) +':'+ str(reading[3])
print(f'Sending result = {sending_str} ...')
# FIXME: send the result and print the server response
sock.sendto(sending_str.encode(), server_addr)
server_response = sock.recv(1024)
print('Respuesta del servidor: '+server_response.decode())

sock.close()
