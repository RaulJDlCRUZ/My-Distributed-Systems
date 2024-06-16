#!/usr/bin/python3

import socket
import struct


def deserialize_reading(data):
    '''Deserializar 16 bits, Byte sin signo, float, Byte sin signo'''
    format_ = "!hBfB"
    # Se calcula cuántos bytes hay que desempaquetar y cómo
    fixed = struct.calcsize(format_)
    # Se establecen las variables y se deserializa [0,fixed)
    id_, type_, value, unit_len = struct.unpack(format_, data[:fixed])
    # Y desde el siguiente elemento se obtienen otros {longitud unidad} más
    unit = data[fixed:][:unit_len]
    # Dicha última cadena se devuelve codificada
    return id_, type_, value, unit.decode()


# Método principal
def main():
    # Apertura y escucha del socket servidor UDP
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('', int(2000)))

    while 1:
        data, client = sock.recvfrom(1024)
        print("New message {}".format(client))
        
        # Deserializar el mensaje
        reading = deserialize_reading(data)
        # Imprimir la tupla resultante, por elementos, dejando 2 decimales en value
        print("Sensor {0} ({1}) value:{2:.2f} {3}".format(*reading))

# Control de interrupciones de teclado
try:
    main()
except KeyboardInterrupt:
    pass
