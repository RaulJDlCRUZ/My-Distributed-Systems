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