# Cliente hablará con el servidor hasta que uno escriba 'bye'
import socket

QUIT = b"bye"

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# El cliente no abre un socket en un puerto, especificamos una tupla de destino
server = ('', 12345)

while 1:
    # Rol de cliente
    message_out = input().encode() # Leer por consola
    sock.sendto(message_out, server)

    if message_out == QUIT:
        break
    
    # Rol de servidor
    message_in, peer = sock.recvfrom(1024)
    print(message_in.decode())

    if message_in == QUIT:
        break
