# Se podrán leer y recibir cuantos mensajes quieran (chat UDP por turnos). Termina con 'bye'!!
import socket

QUIT = b'bye'

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# Servidor asocia el socket a un puerto determinado
sock.bind(('', 12345))
# Ejecución infinita
while 1:
    # Rol de servidor, mensaje entrante
    message_in, peer = sock.recvfrom(1024)
    print(message_in.decode())

    # Comprobación de cierre
    if message_in == QUIT:
        break

    # Cambio de rol, ahora es saliente (cliente)
    message_out = input().encode() # Leer por consola
    sock.sendto(message_out, peer)

    # Si se despide, cerrar
    if message_out == QUIT:
        break
sock.close()
