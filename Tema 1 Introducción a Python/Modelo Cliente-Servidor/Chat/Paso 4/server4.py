# Cada entrada es un hilo adicional, el hilo principal atiende la entrada desde el socket
import socket
import _thread
server = ('', 12345)
QUIT = b"bye"


class Chat:
    '''Estos métodos constituyen la aplicación UDP'''

    def __init__(self, sock, peer):
        '''Constructor'''
        self.sock = sock
        self.peer = peer

    def run(self):
        '''Método de ejecución del chat del servidor'''
        # Cuando se crea el hilo, se ordena llamar al método de envío (rol -> cliente)
        _thread.start_new_thread(self.sending, ())
        # Esto y lo anterior funcionando a la vez
        self.receiving()
        self.sock.close()

    def sending(self):
        '''Método de envío'''
        while 1:
            message = input().encode()
            self.sock.sendto(message, self.peer)
            # Si el envío resulta ser QUIT, se cierra el cliente (fin hilo?)
            if message == QUIT:
                break

    def receiving(self):
        '''Método de recepción'''
        while 1:
            message, peer = self.sock.recvfrom(1024)
            print(message.decode())
            # Si el servidor recibe un mensaje de "bye", se comunica a cliente y sale (a close())
            if message == QUIT:
                self.sock.sendto(QUIT, self.peer)
                break


# Ejecución principal del script
if __name__ == '__main__':
    # Socket UDP
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # Pide permiso al SO para escuchar cualquier IP en puerto 12345
    sock.bind(server)
    # Espera a la llegada de un mensaje, pero solo me interesa la dirección del cliente (MSG_PEEK)
    message, client = sock.recvfrom(0, socket.MSG_PEEK)
    # Se ejecuta una nueva INSTANCIA para el chat
    Chat(sock, client).run()
