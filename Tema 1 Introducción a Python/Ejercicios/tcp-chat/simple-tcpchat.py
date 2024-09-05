#!/usr/bin/python3
import sys
import socket
import argparse


class Messenger:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def exit_request(self, msg):
        return msg.lower() == 'exit'

    def send_msg(self):
        msg = input("Tú: ")
        self.s.send(msg.encode())
        if self.exit_request(msg): self.close()

    def recv_msg(self):
        msg = self.s.recv(1024).decode()
        print(f"Otro: {msg}")
        if self.exit_request(msg): self.close()

    def close(self):
        print("Cerrando conexión...")
        self.s.close()
        sys.exit(0)


class Client(Messenger):
    def __init__(self, host, port):
        super().__init__(host, port)

    def start(self):
        self.s.connect((self.host, self.port))

        while 1:
            self.send_msg()
            self.recv_msg()


class Server(Messenger):
    def __init__(self, host, port):
        super().__init__(host, port)

    def bind(self):
        self.s.bind((self.host, self.port))
        self.s.listen(5)

    def start(self):
        self.bind()
        self.s, addr = self.s.accept()
        print(f"Conexión establecida con {addr}")

        while 1:
            self.recv_msg()
            self.send_msg()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--client', action='store_true')  # on/off flag
    parser.add_argument('-i', '--ip', default='localhost')
    parser.add_argument('-p', '--port', type=int, default=5555)
    args = parser.parse_args()

    messenger_class = Client if args.client else Server
    messenger = messenger_class(args.ip, args.port)
    messenger.start()