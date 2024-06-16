# Sockets BSD

Los sockets se usan casi en cualquier parte, pero son una de las tecnologías peor comprendidas. Sólo se van a tratar los sockets INET (es decir, IPv4), pero éstos representan el 99 % de los sockets que se usan. Y sólo se hablará de los STREAM sockets.

## **`mysocket`**

Suponiendo que no quiere terminar la conexión, la solución más simple es utilizar mensajes de longitud fija. El código de envío de este ejemplo se puede usar para casi cualquier esquema de intercambio de mensajes –en Python puede enviar cadenas, y puede usar
`len()` para obtener la longitud (incluso si tiene caracteres `'\0'`).

Cuando una llamada a `recv()` devuelve 0 bytes, significa que el otro lado ha cerrado (o está cerrando) la conexión. No recibirá más datos en esta conexión, ya que "se ha roto".

```python
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
```