#!/usr/bin/python3

import socket

class mysocket:
    """SOLO PARA DEMOSTRACION - codificado asi por claridad, no por eficiencia"""

    def __init__(self, sock=None):
        self.sock = sock or socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(host, port):
        self.sock.connect((host, port))

    def mysend(msg):
        totalsent = 0
        while totalsent < MSGLEN:
            sent = self.sock.send(msg[totalsent:])
            if sent == 0:
                raise RuntimeError("conexión interrumpida")
            totalsent = totalsent + sent

    def myreceive():
        msg = bytes()
        while len(msg) < MSGLEN:
            chunk = self.sock.recv(MSGLEN - len(msg))
            if chunk == b'':
                raise RuntimeError("conexion interrumpida")
            msg = msg + chunk
        return msg
