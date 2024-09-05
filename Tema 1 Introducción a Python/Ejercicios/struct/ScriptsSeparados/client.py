#!/usr/bin/python3
import socket
import struct
import random
import sys
import argparse

# Parseador de argumentos
parser = argparse.ArgumentParser()
parser.add_argument("-i", "--ip", type=str, required=True,
                    dest="ip", help="IP a usar")
parser.add_argument("-p", "--port", type=int, required=True,
                    dest="port", help="Puerto a usar")


def client(dest_address, dest_port, sequence):
    """Método que recibe una palabra y lo envía a la conexión"""
    send_word = sequence.encode()
    len_msg = len(send_word)

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client_socket:
        send_data = struct.pack(f'!h{str(len_msg)}s', len_msg, send_word)
        # Se envían los datos empaquetados a tupla ip-puerto
        client_socket.sendto(send_data, (str(dest_address), int(dest_port)))


def random_word():
    """Función chorra para sacar una palabra al azar (de los 5 primeros parrafos de Lorem)"""
    with open("../lorem.txt", "r", encoding='utf-8') as file:
        all_words = file.read()
        words = list(all_words.split())
        return random.choice(words)
    # También puede hacerse más simple, sacando palabras de una lista por ejemplo:
    # words = ['hello world', 'meh', 'struct', "ñandú"]
        
if __name__ == "__main__":
    match len(sys.argv):
        case 2:  # si no es para ayuda, error
            parser.print_help()
            if sys.argv[1] != '-h' and sys.argv[1] != '--help':
                sys.exit(1)
        case 5:  # toma y comprueba ip-puerto
            # Llevo al parseador los argumentos
            args = parser.parse_args(sys.argv[1:])
            # Llamo a la función de generación de palabra aleatoria
            new_word = random_word()
            print(f'Enviando palabra: {new_word}')
            client(args.ip, args.port, new_word)
        case _:  # cualquier otro número de argumentos es error
            parser.print_help()
            sys.exit(1)