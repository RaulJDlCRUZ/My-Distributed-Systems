#!/usr/bin/python3 -u
# AUTOR = RAÚL JIMÉNEZ DE LA CRUZ
"Usage: {0} <host> <port>"
import sys
import socket
import struct

server_addr = (sys.argv[1], int(sys.argv[2]))


def deserialize_reading(data):
    '''Esta función deserializa los datos proporcionados por el servidor.
    Para los bytes desempaquetados se calcula previamente los tamaños de los tipos de variables
    con una función incorporada de struct'''
    # PASO 1: LONGITUD DE LA CADENA DEL COLOR
    len_received, = struct.unpack('!f', data[:struct.calcsize('f')])
    # lo convierto a entero para concretar longitud en formato cadena
    len_received = int(len_received)
    # PASO 2: EXTRAER CADENA
    color, = struct.unpack(f'!{str(len_received)}s', data[struct.calcsize(
        'f'):struct.calcsize('f')+len_received])
    # PASO 3: EXTRAER HORA EXACTA
    hour, minute, second, = struct.unpack(
        '!ilh', data[struct.calcsize('f')+len_received:struct.calcsize('f') +
                     len_received+struct.calcsize('ilh')])

    # Los pasos 2 y 3 se pueden comprimir en un solo paso, ya que lo importante es saber primer cuánto de largo es
    # el color proporcionado por el servidor. Luego ya en ese unpack podemos hacer lo demás, son tamaños constantes:
    
    # color,hour, minute, second, = struct.unpack(f'!{str(len_received)}silh', data[struct.calcsize('f'):)
    #                                           cadena de longitud len_received, Integer, Long, sHort.
    
    # NOTA: struct.calcsize('f') se puede sustituir y simplificar por 4.

    # DEVOLVER DATOS
    return color, hour, minute, second


if len(sys.argv) != 3:
    print(__doc__.format(__file__))
    sys.exit(1)

uclm_id = 'Raul.Jimenez'  # if your email is John.Doe@alu.uclm.es

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

print('Sending UCLM ID...')
msg = 'UID'.encode() + uclm_id.encode()
sock.sendto(msg, server_addr)

msg = sock.recv(1024)
reading = deserialize_reading(msg)
sending_str = 'RES' + reading[0].decode() + ' ' + str(reading[1]) + \
    ':' + str(reading[2]) + ':' + str(reading[3])
print(f'Sending result = {sending_str} ...')
sock.sendto(sending_str.encode(), server_addr)
server_response = sock.recv(1024)
print('Respuesta del servidor: '+server_response.decode())

sock.close()
