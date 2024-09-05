Dada la siguiente especificación de protocolo:

```
syntax = "proto3";

message Person {
    string name = 1;
    int32 dni = 2;
    repeated string email = 3;  // john.doe, alu, uclm, es
}

message Result {
    enum Value {
       UNKNOWN = 0;
       OK = 1;
       ERROR = 2;
    }

    Value value = 1;
}
```

Desarrollar un cliente que pueda comunicarse con un servidor que siga este mismo protocolo (asumir que ya existe). Concretamente se debe de enviar al servidor:

- Nombre completo
- DNI
- Correo de la universidad