# El cliente debe esperar la respuesta.
import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.sendto("hola".encode(), ('127.0.0.1', 12345))
# Imitamos al servidor, esperamos al mensaje de respuesta
message, peer = sock.recvfrom(1024)
# Para sacarlo por pantalla
print("{} from {}".format(message.decode(), peer))
sock.close()