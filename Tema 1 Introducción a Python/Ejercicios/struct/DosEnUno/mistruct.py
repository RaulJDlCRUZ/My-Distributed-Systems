#!/usr/bin/python3
import socket
import sys
import argparse
import struct
import signal

SERV_PORT = 8880

def signal_handler(sig, frame):
    '''Método ejecutado al instalar el manejador de la señal de interrupción. Cerrar con error'''
    print(f'\nPrograma interrumpido a causa de la señal de interrupción {sig}')
    sys.exit(-1)

def client(dest_address, dest_port, message):
    """Método correspondiente al cliente, quien envía el mensaje"""
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client_socket:
        # IMPORTANTE EL ORDEN. CODIFICO Y LUEGO CALCULO LA LONGITUD. AL REVÉS PUEDEN FALTAR LETRAS!
        send_word = message.encode()
        len_msg = len(send_word)
        # El formato es ordenamiento de red, entero de 16 bits (cuyo valor es igual a la longitud
        # de la cadena a enviar, aunque no importa) y una cadena de igual longitud.
        send_data = struct.pack(f'!h{str(len_msg)}s', len_msg, send_word)
        # Se envían los datos empaquetados a tupla ip-puerto
        client_socket.sendto(send_data, (str(dest_address), int(dest_port)))


def server():
    """Método correspondiente con el servidor, quien lo recibe y decodifica"""
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server_socket:
        server_socket.bind(("", SERV_PORT))
        print(f'Servidor abierto en el puerto {SERV_PORT}')
        # Servidor abierto, se ejecuta indefinidamente
        while True:
            recv_data, addr = server_socket.recvfrom(1024)
            # Tras llegar los datos, desempaquetamos primero la longitud de la cadena
            # que son 16 bits = 2 bytes. Entonces, como nos llegan bytes empaquetados,
            # aprovechamos y sacamos los primeros 2 (0 y 1) para asignarlo a la longitud
            # IMPORTANTE LA COMA A LO ÚLTIMO, EL DESEMPAQUETADO DEVUELVE UNA TUPLA!!
            len_received, = struct.unpack('!h', recv_data[:2])
            # Con la longitud conocida, desempaquetamos el resto, respetando el resto del
            # formato, y siguiendo por el byte 2, hasta el final.
            message_received, = struct.unpack(f'!{str(len_received)}s', recv_data[2:])
            # Salida por pantalla del resultado, decodificando ahí mismamente
            print(f'Mensaje recibido: {message_received.decode()} ({str(len_received)} bytes) desde {addr}')


# Parseador de argumentos
parser = argparse.ArgumentParser()

# Argumento de modo de ejecución
parser.add_argument("-m", "--mode", type=str, choices=[
                    'server', 'client'], required=True, dest="mode", help='Establecer rol de la ' +
                    'comunicación')


if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
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
