#!/usr/bin/python3

import socket
import sys
import argparse


def client():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as c:
        c.sendto(b"Hola", ("localhost", 8808))  # Esa b es como decir .encode()
        print("Enviado")
        # Ahora al ser un 2 en 1, no puedo cerrar


def server():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.bind(("", 8808))  # tupla ip-puerto
        msg, addr = s.recvfrom(1024)  # tamanyo buffer de entrada
        print(msg.decode())


parser = argparse.ArgumentParser()
parser.add_argument(
    "-m", "--mode",
    type=str,
    default="server",
    required=False,
)

args = parser.parse_args()
server() if args.mode == "server" else client()
