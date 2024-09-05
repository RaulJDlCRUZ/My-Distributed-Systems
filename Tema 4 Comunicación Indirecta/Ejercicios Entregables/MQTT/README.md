Formato del mensaje
====
```
{
  'code': '000000',
  'fullname': 'John Doe',
  'dni': '12345678'  # 8 caracteres (sin letra)
}
```

Interacción (Flujo)
====

```
Code topic                  Publicador              Results topic
     |        code             |                         |
     |------------------------>|                         |   <-+
     |                         |                         |     |  4 seconds max.
     |                         |       JSON message      |     |
     |                         |------------------------>|   <-+
     |                         |                         |
```

_Topics_
====

```
Code topic:
ssdd/ejercicio004/person/code

Results topic:
ssdd/ejercicio004/person/result
```