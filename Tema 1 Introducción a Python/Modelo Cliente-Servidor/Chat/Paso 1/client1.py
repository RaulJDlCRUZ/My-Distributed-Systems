# Implementar un cliente UDP que debe enviar la cadena ‘hello’ al servidor anterior y terminar.
'''
Comando que sustituye o simplifica a este cliente
    $ echo hola | ncat --udp --send-only 127.0.0.1 12345
'''
import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.sendto("hola".encode(), ('127.0.0.1', 12345))
sock.close()
