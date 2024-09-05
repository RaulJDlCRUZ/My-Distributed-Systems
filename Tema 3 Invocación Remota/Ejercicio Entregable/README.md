```
server                                       client
  |                                            |
  |          RequestRandomNumber(email)        |
 +++ <--------------------------------------- +++
 | |                                          | |
 | |                                          | |
 | |             (random number)              | |
 +++ ---------------------------------------> +-+
  |                                            |-----+
  |                                            |     | result = factorial(number)
  |        CheckFactorial(email, result)       |-----+
 +++ <--------------------------------------- +++
 | |                                          | |
 | |                                          | |
 | |                 (result)                 | |
 +++ ---------------------------------------> +-+
```

Desarrollar un cliente que permita obtener de un servidor remoto un número aleatorio, para que el cliente calcule su número factorial:

$$

n! = n \times (n-1) \times (n-2) ... \times 3 \times 2 \times 1

$$

una vez calculado, se enviará al servidor, junto al email, para obtener una respuesta.

El protocolo empleado es el siguiente:

```
syntax = "proto3";

package factorial_checker;

service FactorialChecker {
  rpc RequestRandomNumber(NumberRequest) returns (NumberResponse) {}
  rpc CheckFactorial(CheckRequest) returns (CheckResponse) {}
}

message NumberRequest {
  string email = 1;
}

message NumberResponse {
  int32 number = 1;
}

message CheckRequest {
  string email = 1;
  int64 factorial = 2;
}

message CheckResponse {
  string result = 1;
}
```