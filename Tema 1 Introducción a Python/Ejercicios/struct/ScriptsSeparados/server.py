#!/usr/bin/python3
import socket
import struct
import sys


def server():
    """Procedimiento infinito del servidor. Recibe y decodifica"""
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server_socket:
        server_socket.bind(("", 8880))
        # Servidor abierto, se ejecuta indefinidamente
        while True:
            recv_data, addr = server_socket.recvfrom(1024)
            len_received, = struct.unpack('!h', recv_data[:2])
            message_received, = struct.unpack(
                f'!{str(len_received)}s', recv_data[2:])
            print(
                f'Mensaje recibido: {message_received.decode()} ({str(len_received)} bytes) desde {addr}')


if __name__ == "__main__":
    if len(sys.argv) != 1:
        print("Uso: python3 server.py")
        sys.exit(-1)
    else:
        server()
