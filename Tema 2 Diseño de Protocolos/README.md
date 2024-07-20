# Tema 2: Diseño de Protocolos

## Google Protocol Buffers

- Utilizado en muchos servicios orientados a datos.
- Marshalling binario: mensajes pequeños y procesado rápido
- Compatibilidad con muchos lenguajes y con versiones anteriores: la nueva versión del protocolo debería trabajar con programas heredados
- Gestiona la serialización de las estructuras del lenguaje de programación a secuencias binarias y viceversa. Tipos incorporados:
    - `bool`, `string`, `int32`, `int64`, `float`, `double`, etc.
    - Enumerations, _nested_, _any_, _oneof_, _maps_, etc.

### `struct`

Descripción: El cliente UDP emite lecturas de sensores al servidor

#### Servidor

```python
#!/usr/bin/python3
import socket
import struct

def deserialize_reading(data):
    '''Deserializar 16 bits, Byte sin signo, float, Byte sin signo'''
    format_ = "!hBfB"
    fixed = struct.calcsize(format_)
    id_, type_, value, unit_len = struct.unpack(format_, data[:fixed])
    unit = data[fixed:][:unit_len]
    return id_, type_, value, unit.decode()


# Método principal
def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('', int(2000)))

    while 1:
        data, client = sock.recvfrom(1024)
        print("New message {}".format(client))
        
        reading = deserialize_reading(data)
        print("Sensor {0} ({1}) value:{2:.2f} {3}".format(*reading))

# Control de interrupciones de teclado
try:
    main()
except KeyboardInterrupt:
    pass
```

**Ejecutar**

```console
socket.struct$ ./udp-server.py
New message ('127.0.0.1', 36137)
Sensor 8 (2) value:16.30 bar
```

#### Cliente

```python
#!/usr/bin/python3
import sys
import socket
import struct

# Constantes de tipo de sensor
UNKNOWN = 0
HUMIDITY = 1
PRESSURE = 2
ACCELERATION = 3

def serialize_reading(id_, type_, value, unit):
    '''Serializar 16 bits, Byte sin signo, float, Bytes sin signo (constante de arriba),
    string de cadena con longitud = unit (puesto con {})'''
    unit = unit.encode()
    unit_len = len(unit)
    return struct.pack('!hBfB{}s'.format(unit_len), id_, type_, value, unit_len, unit)

if len(sys.argv) != 2:
    print(__doc__.format(__file__))
    sys.exit(1)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
data = serialize_reading(id_=8, type_=PRESSURE, value=16.3, unit='bar')
print(data)
sock.sendto(data, (sys.argv[1], 2000))
sock.close()
```

**Ejecutar**

```console
socket.struct$ ./udp-client.py localhost
b'\x00\x08\x02A\x82ff\x03bar'
```

### `protobuf`

Descripción: El cliente UDP emite lecturas de sensores al servidor

```proto
syntax = "proto3";

message Reading {
    int32 Id = 1;

    enum SensorType {
       UNKNOWN  = 0;
       HUMIDITY = 1;
       PRESSURE = 2;
       ACCELERATION = 3;
    }

    SensorType type = 2;
    float value = 3;
    string unit = 4;
}
```

**Compilar**

```console
socket.protobuf$ make protoc -I . --python_out=. sensor.proto
```

#### Servidor

```python
from sensor_pb2 import Reading

sock = socket.socket(type=socket.SOCK_DGRAM)
sock.bind(('', 2002))
reading = Reading()

while True:
    data, address = sock.recvfrom(1024)
    print(f"sensor: {address}, raw-data: {data}")

    # Se lleva al sensor los datos brutos
    reading.ParseFromString(data)
    # Se imprime una vez procesado/formateado
    print("Sensor {0.Id} ({1}) value:{0.value:.2f} {0.unit}".format(
        reading, Reading.SensorType.Name(reading.type)))
```

**Ejecutar**

```console
socket.protobuf$ ./udp-server.py
sensor: ('127.0.0.1', 53957), raw-data: b'\x08\x01\x10\x01\x1d\xcd\xccL>"\x05kg/m3'
Sensor 1 (HUMIDITY) value:0.20 kg/m3
```

#### Cliente

```python
import sensor_pb2

if len(sys.argv) < 2:
    print('Usage: ./uddp-client.py <host>')
    exit()

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
destination = (sys.argv[1], 2002)

# Llamada a método lectura del sensor protobuf (IMPORTANTE SABER SU PROTOCOLO)
reading = sensor_pb2.Reading()
# Definición de campos a enviar: ID, TIPO, VALOR, UNIDADES
reading.Id = 1
reading.type = sensor_pb2.Reading.HUMIDITY
reading.value = 0.2
reading.unit = "kg/m3"

# Mandamos a serializar al sensor, se imprime (b'') y envía
data = reading.SerializeToString()
print(data)
sock.sendto(data, destination)
sock.close()
```

**Ejecutar**

```console
socket.protobuf$ ./udp-client.py localhost
```

## Ejercicios de protocolos

### 1\. Puerta de garaje

Tenemos una puerta de garaje abatible de dos hojas que se va a operar mediante un mando inalámbrico. La centralita solo ofrece 3 operaciones: **abrir**, **cerrar** y **consultar estado**. El control devolverá un error tanto al solicitar apertura como cierre si la puerta ya está en ese estado. El comando de apertura tiene 2 modos: vehículo y peatón (en el que solo se abre una de las hojas). El mando puede indicar el tiempo que la puerta permanece abierta, en caso contrario quedará abierta indefinidamente. La centralita responderá siempre a cada comando con un _OK_ o código de error. Los posibles errores son:

- La puerta ya está abierta
- La puerta ya está cerrada
- Se encontró un obstáculo
- El motor no responde

Diseña un protocolo binario que permita la funcionalidad indicada. Después, impleméntalo con ProtocolBuffers

### 2\. Instawhat

Instawhat es una red social en la que un usuario puede publicar una fotografía que haya encontrado en internet indicando su URL pública. Para esa fotografía, otros usuarios pueden comentar, puntuar o dar a "me gusta". Además, el usuario que publicó la foto puede eliminarla de la red social, aunque seguirá existiendo en el sitio externo. La red social solamente te permite ver las últimas 20 fotos publicadas por cualquier usuario.

Diseña un protocolo binario que permita la funcionalidad indicada. Después, impleméntalo con ProtocolBuffers.

_[Solución](./Ejercicios%20de%20protocolos/Instawhat-Paula/) propuesta por [Paula Castillejo](https://github.com/PAULACASTILLEJOBRAVO)_