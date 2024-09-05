# Cambiar ligeramente para que el servidor pueda contestar al cliente (chat UDP con respuesta)
import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('', 12345))
message, peer = sock.recvfrom(1024)
print(message.decode(), peer)
# Contestamos al cliente
sock.sendto("qué tal?".encode(), peer)
sock.close()
