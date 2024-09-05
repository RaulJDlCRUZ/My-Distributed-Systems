#!/usr/bin/env python3

import socket
from sensor_pb2 import Reading

# Socket UDP que aceptará clientes
sock = socket.socket(type=socket.SOCK_DGRAM)
sock.bind(('', 2002))
# NUevo objeto de la lectura del sensor
reading = Reading()

while True:
    data, address = sock.recvfrom(1024)
    print(f"sensor: {address}, raw-data: {data}")

    # Se lleva al sensor los datos brutos
    reading.ParseFromString(data)
    # Se imprime una vez procesado/formateado
    print("Sensor {0.Id} ({1}) value:{0.value:.2f} {0.unit}".format(
        reading, Reading.SensorType.Name(reading.type)))
