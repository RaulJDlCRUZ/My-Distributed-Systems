# Cliente de chat UDP simultáneo
import socket
# Me interesa la tupla ip-puerto del servidor y la instancia Chat
from server4 import Chat, server

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
Chat(sock, server).run()
