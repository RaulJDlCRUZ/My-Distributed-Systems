# Ejercicio de Sockets Curso 2023/24

<pre>

             Server                                   Client
               |             'UID' + user_id            |
               |<---------------------------------------| --- (example: 'UID' + 'John.Doe')
               |                                        |
               |                   msg                  |
               |--------------------------------------->|
               |                                        |----+
               |                                        |    | msg data
               |                                        |    | unmarshalling ----------
               |                                        |<---+                        | formatted as str...
               |    'RES' + " ::"    |                             v
               |<---------------------------------------| --- (example: 'RES' + 'red 12:34:56')
          +----|                                        |
 check if |    |                                        |
  data ok |    |                                        |
          +--->|                                        |
               |      check result: 'OK' or 'FAIL'      |
               |--------------------------------------->|
               |                                        |

</pre>

---

Formato del primer mensaje (msg) recibido del servidor:

```
1. color lenght - float
2. color name   - string
3. hour         - int
4. minute       - long
5. second       - short
```

Todos los números tienen signo

Código proporcionado:

```python
#!/usr/bin/python3 -u
"Usage: {0} <host> <port>"

import sys
import socket


server_addr = (sys.argv[1], int(sys.argv[2]))


def deserialize_reading(data):
    # FIXME: complete this function for data unmarshalling

    # Your code here

    return color, hour, minute, second


if len(sys.argv) != 3:
    print(__doc__.format(__file__))
    sys.exit(1)

# FIXME: write your own UCLM ID
uclm_id = 'John.Doe'  # if your email is John.Doe@alu.uclm.es

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

print('Sending UCLM ID...')
msg = 'UID'.encode() + uclm_id.encode()
sock.sendto(msg, server_addr)

msg = sock.recv(1024)
reading = deserialize_reading(msg)

print('Sending result...')

# FIXME: send the result and print the server response

sock.close()
```

> También se proporciona una posible implementación del servidor que probablemente se usó durante la sesión evaluable