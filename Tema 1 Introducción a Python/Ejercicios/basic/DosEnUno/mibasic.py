#!/usr/bin/python3
import socket
import sys
import argparse


def client(ip_dir, dest_port, msg):
    """Método que ejecuta el cliente."""
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client_socket:
        # Socket cliente envía el mensaje codificado en utf-8, hacia la tupla ip-puerto
        # La IP es una cadena, y el puerto es un entero, lo casteamos
        client_socket.sendto(msg.encode('utf-8'),
                             (str(ip_dir), int(dest_port)))
        print("Enviado")
        # Ahora al ser un programa 2 en 1, no puedo cerrar con exit()


def server():
    """Método que ejecuta el servidor."""
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server_socket:
        server_socket.bind(("", 8808))  # tupla ip-puerto
        # Servidor abierto, funcionando infinitamente hasta el cierre del script
        while True:
            # buffer de entrada con tam = 1024
            msg, addr = server_socket.recvfrom(1024)
            # reemplaza por ??, ignore directamente no los escribe
            print('"'+msg.decode(encoding="ascii", errors="replace")+'"', addr)


# Parseador de argumentos
parser = argparse.ArgumentParser()

# Nuevo argumento: modo de ejecución:
'''
En primer lugar, no añado un argumento de ayuda, por defecto ya existe.
Entonces, nuestro único argumento es el modo (escrito como -m o --mode) de ejecución.
Aceptará como tipo una cadena, para especificar si es cliente o servidor, de hecho sólo son
admitidas esas opciones. Es un argumento obligatorio o requerido, y en la ayuda mostrará qué
significa --mode.
'''

parser.add_argument("-m", "--mode", type=str, choices=[
                    'server', 'client'], required=True, dest="mode", help='Establecer rol de la ' +
                    'comunicación')

# Método main.
# Se ejecuta cuando ejecutamos el script,
# no al importarlo como módulo.
if __name__ == "__main__":
    match len(sys.argv):  # Comprobar el número de argumentos
        case 2:  # Sólo tiene sentido para --help
            parser.print_help()
            if sys.argv[1] != '-h' and sys.argv[1] != '--help':
                sys.exit(1)
        case 3:  # El indicado para el rol, los llevamos a comprobar al parser
            args = parser.parse_args(sys.argv[1:])
            match args.mode:  # Seleccionar el modo
                case'server':
                    # Llamada a función servidor, el puerto es arbitrario
                    server()
                case 'client':
                    # La tupla ip-puerto la sacamos con una cadena dividida por ':'
                    # Si fallase, cierra con error
                    address, port = input('Escribe la ip y puerto a conectar con el formato' +
                                          ' <ip:puerto>\n').split(':')
                    # Mensaje a enviar
                    chain = input('Escribe el mensaje a enviar: ')
                    # Llamada a la función cliente
                    client(address, port, chain)
        case _:  # Default
            parser.print_help()
            sys.exit(1)
