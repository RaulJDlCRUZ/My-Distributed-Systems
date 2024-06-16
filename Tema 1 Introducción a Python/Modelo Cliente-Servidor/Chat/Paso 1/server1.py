# Implementar un servidor UDP que ha de recibir un único mensaje, imprimirlo en consola y terminar.
import socket

# Crear socket UDP (AF_INET = familia protocolos Internet, SOCK_DGRAM = Protocolo con datagramas)
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# Vinculación del socket a un puerto libre = 12345
sock.bind(('', 12345))
# Bloqueado hasta que llegue un datagrama, que contiene el mensaje de texto
message, client = sock.recvfrom(1024)
# Imprimir el mensaje recibido por consola
print(message.decode(), client)
# Cerrar el socket
sock.close()
