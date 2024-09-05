#!/usr/bin/python3

import socket
import sys
import argparse


def client():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as c:
        # Esa b es como decir .encode()
        c.sendto('Ñandúomega'.encode('utf-8'), ("localhost", 8808))
        print("Enviado")
        # Ahora al ser un programa 2 en 1, no puedo cerrar con exit()


def server():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.bind(("", 8808))  # tupla ip-puerto
        msg, addr = s.recvfrom(1024)  # tamanyo buffer de entrada
        # print(msg.decode(encoding="ascii", errors="ignore")) # Opción para ignorar char inadmitidos
        # Opción para reemplazar char inadmitidos por ??
        print(msg.decode(encoding="ascii", errors="replace"))


parser = argparse.ArgumentParser()
parser.add_argument(
    "-m", "--mode",
    type=str,
    default="servidor",
    required=False,
)

args = parser.parse_args()
server() if args.mode == "servidor" else client()
