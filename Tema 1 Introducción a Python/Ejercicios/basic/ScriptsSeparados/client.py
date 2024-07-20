#!/usr/bin/python3
import socket
import sys
import argparse

# Parseador de argumentos
parser = argparse.ArgumentParser()
parser.add_argument("-i", "--ip", type=str, required=True,
                    dest="ip", help="IP a usar")
parser.add_argument("-p", "--port", type=int, required=True,
                    dest="port", help="Puerto a usar")


def client(address, dest_port, message):
    """Creación del socket cliente y envío del mensaje"""
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client_socket:
        # Socket cliente envía el mensaje codificado en utf-8, hacia la tupla ip-puerto
        # La IP es una cadena, y el puerto es un entero, lo casteamos
        client_socket.sendto(message.encode('utf-8'),
                             (str(address), int(dest_port)))
        print(f'Se ha enviado "{message}"')
        # Ahora al ser un programa 2 en 1, no puedo cerrar con exit()


if __name__ == "__main__":
    match len(sys.argv):
        case 2:  # si no es para ayuda, error
            parser.print_help()
            if sys.argv[1] != '-h' and sys.argv[1] != '--help':
                sys.exit(1)
        case 6:  # toma y comprueba los valores
            # Llevo al parseador los argumentos de tipo "--", el último argumento va aparte
            args = parser.parse_args(sys.argv[1:5])
            client(args.ip, args.port, sys.argv[5])
        case _:  # cualquier otro número de argumentos es error
            parser.print_help()
            sys.exit(1)
