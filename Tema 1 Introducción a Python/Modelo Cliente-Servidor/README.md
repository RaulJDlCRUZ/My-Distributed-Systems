# El modelo Cliente-Servidor

La mayoría de los protocolos clásicos de aplicación de Internet (HTTP, FTP, IMAP, SMTP, etc.) están basados en este modelo, y a día de hoy, la mayoría de aplicaciones que utilizamos siguen aplicando esta misma arquitectura básica. En este modelo se asumen dos roles bien diferenciados:

- El **servidor** es la parte _pasiva_. Permanece inactiva a la espera de una petición para realizar una tarea o porveer un recurso a través de la red.
- El **cliente** es la parte _activa_. Establece una conexión o envía una petición a un servidor para que éste realice la tarea especificada o bien le proporcione acceso a un recurso remoto.

El modelo cliente-servidor implica un patrón de comunicación característico conocido como **petición-respuesta**. En éste, el cliente realiza una petición —que puede incluir un identificador de un recurso y una operación— y el servidor devuelve una respuesta con un resultado o un código indicando si la operación se pudo realizar satisfactoriamente o se produjo un error.<br>
El formato de estos mensajes de petición y respuesta está especificado en un protocolo de aplicación.

## Chat

Una de las aplicaciones de red más simples que se puede programar es un chat, es decir, un programa que permite a dos personas intercambiar mensajes de texto a través de la red.

### Paso 1: Mensaje unidireccional

- Implementar un cliente UDP que debe enviar la cadena `'hello'` al servidor anterior y terminar.

    ```python
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto("hello".encode(), ('127.0.0.1', 12345))
    sock.close()
    ```

    Equivale al siguiente comando UNIX:

    ```console
    $ echo hello | ncat --udp --send-only 127.0.0.1 12345
    ```

- Implementar un servidor UDP que ha de recibir un único mensaje, imprimirlo en consola y terminar. Las tareas que ha de realizar el servidor son muy simples:
    1. Crear un socket UDP.
    2. Vincular dicho socket a un puerto libre.
    3. Esperar un datagrama que contiene un mensaje de texto.
    4. Imprimir el mensaje en consola

        ```python
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind(('', 12345))
        message, client = sock.recvfrom(1024)
        print(message.decode(), client)

        sock.close()
        ```


### Paso 2: Lo educado es responder

El servidor del paso anterior sólo imprime el mensaje recibido. Un pequeño cambio le permitirá devolver el saludo al cliente.

Utilizando la dirección del cliente, que se obtiene como valor de retorno del método `recvfrom()`, la aplicación puede a su vez utilizar el método `sendto()` y enviar un mensaje de respuesta al cliente.

#### Cliente

```python
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.sendto("hola".encode(), ('127.0.0.1', 12345))
# Ahora esperamos a la respuesta
message, peer = sock.recvfrom(1024)
print("{} from {}".format(message.decode(), peer))

sock.close()
```

#### Servidor

```python
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('', 12345))
message, peer = sock.recvfrom(1024)
print(message.decode(), peer)
# Contestamos al cliente
sock.sendto("qué tal?".encode(), peer)
sock.close()
```

### Paso 3: Libertad de expresión

Con este paso los usuarios que ejecutan cliente y servidor tendrán realmente la oportunidad de conversar. Para ello, ambos programas deben leer de consola lo que el usuario teclee para enviarlo hacia su interlocutor. Además, podrán enviar cuantos mensajes quieran.<br>
La conversación se mantendrá hasta que cualquiera de ellos envíe la cadena `'bye'`.

#### Cliente

```python
QUIT = b"bye"

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server = ('', 12345)

while 1:
    # Rol de cliente
    message_out = input().encode()
    sock.sendto(message_out, server)

    if message_out == QUIT:
        break
    
    # Rol de servidor
    message_in, peer = sock.recvfrom(1024)
    print(message_in.decode())

    if message_in == QUIT:
        break
```

#### Servidor

```python
QUIT = b'bye'

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('', 12345))

while 1:
    # Rol de servidor, mensaje entrante
    message_in, peer = sock.recvfrom(1024)
    print(message_in.decode())

    if message_in == QUIT:
        break

    # Cambio de rol, ahora es saliente (cliente)
    message_out = input().encode()
    sock.sendto(message_out, peer)

    if message_out == QUIT:
        break
sock.close()
```

### Paso 4: Habla cuando quieras

La versión de la sección anterior tiene un problema grave. Tanto el cliente como el servidor tienen dos puntos diferentes en los que el programa queda bloqueado: la función `input()` para leer de consola y el método `recvfrom()` para leer del socket. Eso implica que ambos han de esperar a que su interlocutor envíe un mensaje antes de poder escribir de nuevo.

Es un problema clásico en software que maneja E/S o comunicaciones. El programa necesita atender al mismo tiempo dos (en este caso) o más fuentes de datos asíncronas, es decir, que pueden enviar datos en cualquier momento. En este tipo de programas se suele asociar un bloque de código (un manejador) a un evento asíncrono (no predecible). 

Este enfoque se denomina _programación dirigida por eventos_.

Existen varias formas de abordar este problema. La que se propone aquí consiste en **atender una de las entradas (la consola) en un hilo adicional mientras que el hilo principal se utiliza para atender la entrada desde el socket**.

#### Servidor

```python
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
        _thread.start_new_thread(self.sending, ())
        self.receiving()
        self.sock.close()

    def sending(self):
        '''Método de envío'''
        while 1:
            message = input().encode()
            self.sock.sendto(message, self.peer)

            if message == QUIT:
                break

    def receiving(self):
        '''Método de recepción'''
        while 1:
            message, peer = self.sock.recvfrom(1024)
            print(message.decode())

            if message == QUIT:
                self.sock.sendto(QUIT, self.peer)
                break
```

El programa está compuesto por una clase **`Chat`** con tres métodos, incluyendo el constructor.
- El método `sending()` se ocupa de leer líneas de texto de la consola y enviarlas a través del socket.
- El método `receiving()` lee líneas de texto del socket y las imprime en la consola.

> En ambos casos si la cadena es 'bye' la función termina

```python
# Ejecución principal del script
if __name__ == '__main__':
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(server)
    message, client = sock.recvfrom(0, socket.MSG_PEEK)
    Chat(sock, client).run()
```

En cuanto a la función principal, la llamada a `recvfrom()` se utiliza únicamente para obtener la dirección del cliente, pero no lee nada del buffer del socket gracias al _flag_ `MSG_PEEK`. Después se crea una instancia de la clase Chat pasando el socket y la dirección del cliente como parámetros.


#### Cliente

```python
# Me interesa la tupla ip-puerto del servidor y la instancia Chat
from server4 import Chat, server

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
Chat(sock, server).run()
```

El cliente solo difiere en la creación del socket. Simplemente crea el socket (pero no lo vincula) y una instancia de la clase **`Chat`** (la misma del servidor), a la que le pasa dicho socket y la dirección del servidor.

### Paso 5: Todo en uno

Podríamos crear un único programa que se comporte como servidor o cliente en función de un parámetro de línea de comandos.

```python
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

    mode = sys.argv[1]
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Modo servidor
    if mode == '--server':
        sock.bind(SERVER)
        message, client = sock.recvfrom(0, socket.MSG_PEEK)
        Chat(sock, client).run()

    # Modo cliente
    else:
        Chat(sock, SERVER).run()
```

## Ejemplos rápidos de sockets

### Un cliente HTTP básico

```python
import socket

s = socket.socket()
s.connect(('insecure.org', 80))
s.send(b"GET /\n")
print(s.recv(2048))
```

### Un servidor HTTP

```python
from http.server import HTTPServer, SimpleHTTPRequestHandler

server = HTTPServer(('', 8000), SimpleHTTPRequestHandler)
print("Open http://{}:{}".format(*server.socket.getsockname()))

try:
    server.serve_forever()
except KeyboardInterrupt:
    server.server_close()
```