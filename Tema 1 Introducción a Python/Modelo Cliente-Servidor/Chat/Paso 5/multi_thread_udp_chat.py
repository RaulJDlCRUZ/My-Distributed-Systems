# Chat multihilo TCP todo en uno. Como el paso 4 pero en main() se especifica el rol
import socket
import _thread
import sys
SERVER = ('', 12345)
QUIT = b'bye'


class Chat:
    def __init__(self, sock, peer):
        self.sock = sock
        self.peer = peer

    def run(self):
        _thread.start_new_thread(self.sending, ())
        self.receiving()
        self.sock.close()

    def sending(self):
        while 1:
            message = input().encode()
            self.sock.sendto(message, self.peer)

            if message == QUIT:
                break

    def receiving(self):
        while 1:
            message, peer = self.sock.recvfrom(1024)
            print("other> {}".format(message.decode()))

            if message == QUIT:
                self.sock.sendto(QUIT, self.peer)
                break


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print(__doc__ % sys.argv[0])
        sys.exit()

    # Si el número de argumentos es correcto (2), el modo se guarda en el segundo
    mode = sys.argv[1]
    # Se crea el socket UDP
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Modo servidor
    if mode == '--server':
        # Se pone a escuchar
        sock.bind(SERVER)
        # Reciben mensaje para obtener cliente
        message, client = sock.recvfrom(0, socket.MSG_PEEK)
        # Ejecutar la INSTANCIA -> hilo para el cliente Y PODER CONTESTAR
        Chat(sock, client).run()

    # Modo cliente
    else:
        # Inicio directo con el hilo para CONVERSAR
        Chat(sock, SERVER).run()
