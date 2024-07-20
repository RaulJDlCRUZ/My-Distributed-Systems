#!/usr/bin/python3
import socket
import signal
import sys
import argparse


# En este caso, se va a desarrollar un chat entre cliente y servidor usando sockets TCP.
# Estos, a diferencia de los UDP, no se denotan como

#     socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# En su lugar, se escriben de la siguiente manera:

#     socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Además, podemos hacerlo en un sólo script, ya que al ser un chat en el que el cliente se alterna
# con el servidor, esperando uno a la espera del otro (bloqueándose), realmente se intercambian los
# roles, por lo que al final resultaría en código duplicado (no deseado)

# Entonces, lo haremos todo en una misma clase, y su uso se alternará a conveniencia (tal y como
# sucede en chats UDP de ejemplo)

def signal_handler(sig, frame):
    '''Método ejecutado al instalar el manejador de la señal de interrupción. Cerrar con error'''
    print(f'\nPrograma interrumpido a causa de la señal de interrupción {sig}')
    sys.exit(-1)


class Tcpmessenger:
    """Clase de la aplicación de mensajería TCP. En resumen, son los métodos atómicos utilizados
       para cualquier operación durante la conversación. Estos son el constructor, la petición de
       cierre, la llegada y envío de un mensaje."""

    def __init__(self, host, port):
        """Método constructor. Inicializa el socket con el IP-Puerto"""
        self.host = host
        self.port = port
        # Creamos el socket TCP (SOCK_STREAM) aquí, no en el main, ya que se ejecutarán instancias
        # de cliente y servidor directamente
        self.misock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def exit_request(self, msg_recv):
        """Petición de salida. Compara las minúsculas de lo tecleado con 'exit'.
           Devuelve True si son iguales"""
        return msg_recv.lower() == 'exit'

    def send_message(self):
        """Método que envía el mensaje. Se pide el mensaje por pantalla y se envía al socket.
           Si resulta ser exit, se cierra el socket"""
        sending_msg = input("  Tú> ")
        self.misock.send(sending_msg.encode())
        if self.exit_request(sending_msg):
            self.close_socket()

    def receive_message(self):
        """Método que procesa la llegada de un mensaje. Básicamente lo imprime.
           También cerrará su socket si resulta ser 'exit'"""
        received_msg = self.misock.recv(1024).decode()
        print('Otro> '+received_msg)
        if self.exit_request(received_msg):
            self.close_socket()

    def close_socket(self):
        """Método que cierra el socket cuando termina la comunicación"""
        print('Cerrando conexión y finalizando el proceso...')
        self.misock.close()
        sys.exit(0)


class Client(Tcpmessenger):
    """Clase de cliente. HERENCIA DE LA APP DE MENSAJERÍA"""

    def __init__(self, host, port):
        super().__init__(host, port)  # Heredar métodos padre (NUEVA INSTANCIA)

    def start(self):
        """Arrancar instancia cliente. Un cliente en el momento en el que inicializa su
           socket, comienza su three-way handshake. Esta operación del protocolo TCP/IP
           se contempla con la instrucción en Python connect(), método al que se le pasa
           el host (ip) y puerto del rol del cliente (SUYO).
           Luego, con un bucle infinito, se van intercambiando mensajes, hasta que hay
           un cierre por parte del cliente o del servidor.
           """
        self.misock.connect((self.host, self.port))

        while True:
            self.send_message()
            self.receive_message()


class Server(Tcpmessenger):
    """Clase del servidor. HEREDA DE LA APP DE MENSAJERÍA"""

    def __init__(self, host, port):
        super().__init__(host, port)  # Heredar métodos padre (NUEVA INSTANCIA)

    def start(self):
        """Arrancar instancia servidor. En un socket TCP, para que el servidor pueda
           escuchar peticiones de clientes, se deben de completar las siguientes fases,
           todas comprendidas en orden en el siguiente método:
                1. bind()   <-- unir la tupla ip (el host) con el puerto (establecer status)
                                En ese momento no debe de estar ya conectado (es el 1er paso)
                2. listen() <-- espera para que un cliente se conecte (definir reserva o
                                número de conexiones máximas)
                3. accept() <-- Cuando el socket está vinculado/configurado, ya puede
                                recibir peticiones. Devuelve el objeto socket preparado
                                para intercomunicarse y la dirección del cliente aceptado
        """
        self.misock.bind(('', self.port))
        self.misock.listen(5)
        self.misock, addr = self.misock.accept()
        print(f'Conexión establecida con {addr}')

        while True:
            self.receive_message()
            self.send_message()


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
                    messenger = Server('localhost', 8808)
                case 'client':
                    # La tupla ip-puerto la sacamos con una cadena dividida por ':'
                    # Si fallase, cierra con error
                    address, port = input('Escribe la ip y puerto a conectar con el formato' +
                                          ' <ip:puerto>\n').split(':')
                    # Llamada a la función cliente
                    messenger = Client(str(address), int(port))
            messenger.start()
        case _:  # Default
            parser.print_help()
            sys.exit(1)
