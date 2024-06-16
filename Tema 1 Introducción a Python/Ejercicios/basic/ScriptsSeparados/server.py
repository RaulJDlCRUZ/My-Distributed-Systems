#!/usr/bin/python3
import socket
import sys


def server():
    """Ejecución del servidor y tratamiento del mensaje recibido"""
    my_port = int(8808)
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server_socket:
        server_socket.bind(("", my_port))  # tupla ip-puerto
        # Servidor abierto, funcionando infinitamente hasta el cierre del script
        print('Servidor abierto por el puerto ', my_port)
        while True:
            # buffer de entrada con tam = 1024
            msg, addr = server_socket.recvfrom(1024)
            # Control de lo que llega del cliente. Si hay caracteres que no pertenecen a ascii
            # Se lanza una excepción de decodificación, informando y prosiguiendo con la
            # siguiente iteración del while True
            try:
                msg = msg.decode('ascii')
            except UnicodeDecodeError as ude:
                print(f'Error desde {addr}: ', ude)
                continue
            print(f'Llegó "{msg}" from {addr}')


if __name__ == "__main__":
    if len(sys.argv) != 1:
        print("Uso: python3 server.py")
        sys.exit(-1)
    else:
        server()
