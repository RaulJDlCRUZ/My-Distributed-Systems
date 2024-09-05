# Tema 4: Comunicación Indirecta

La comunicación directa es punto a punto, es decir, los participantes deben existir al mismo tiempo $\rightarrow$ establecimiento de conexión o sesión. Cada participante requiere una forma de conocer la dirección del otro. Ineficiente cuando hay muchos participantes.

## Sistemas basados en eventos - Paradigma _publicador-suscriptor_

- Los **publicadores** publican eventos estructurados en un servicio de eventos
- Los **suscriptores** expresan interés en eventos particulares a través de suscripciones que pueden ser patrones arbitrarios sobre los eventos estructurados
- El **broker** o servicio de eventos recibe eventos de los publicadores y los entrega a los suscriptores de acuerdo con sus intereses.

### Basado en canales de eventos - ZeroC IceStorm

Los publicadores publican eventos en canales nombrados (designados) y los suscriptores luego se suscriben a uno de estos canales designados para recibir todos los eventos enviados a ese canal. Este es un esquema bastante primitivo y el único que define un canal físico. Ejemplo: ZeroC IceStorm.

> Recomendable consultar [sesión 4 de laboratorio](/Sesiones%20de%20laboratorio/S4%20Canales%20de%20Eventos/README.md)

### Basado en tópicos "Topics" - MQTT

Es muy similar al basado en canales, solo que cada notificación se expresa en términos de una serie de campos, y un campo indica el tópico. Ejemplo: MQTT.

**Requisitos / Dependencias (Debian)**

```console
python3-paho-mqtt
mosquitto
```

**Arrancar servicio `mosquitto`**

```console
$ sudo service mosquitto restart
```

**Publicador I: Humedad**

```python
import paho.mqtt.client as mqtt

IDENTIFIER = 'X001'


def take_reading():
    return {
        'identifier': IDENTIFIER,
        'value': random.randint(60, 80),
        'unit': '% RH',
        'timestamp': time.time()
    }


publisher = mqtt.Client()
publisher.connect('127.0.0.1')

while 1:
    publisher.publish(
        'iotevents/humidity/{}'.format(IDENTIFIER),
        json.dumps(take_reading())
    )

    time.sleep(1)
```

**Publicador II: Temperatura**

```python
import paho.mqtt.client as mqtt

IDENTIFIER = 'X002'


def take_reading():
    return {
        'identifier': IDENTIFIER,
        'value': random.randint(20, 40),
        'unit': 'Celsius',
        'timestamp': time.time()
    }


publisher = mqtt.Client()
publisher.connect('127.0.0.1')

while 1:
    publisher.publish(
        'iotevents/temperature/{}'.format(IDENTIFIER),
        json.dumps(take_reading())
    )

    time.sleep(2)
```

```console
$ python3 publisher-temperature.py & python3 publisher-humidity.py
```

**Suscriptor**

```python
import paho.mqtt.client as mqtt


def callback(client, userdata, message):
    decoded = json.loads(message.payload.decode())
    print("topic: {}, msg: {}".format(
        message.topic, decoded))

    print(decoded["value"])


subscriber = mqtt.Client()
subscriber.on_message = callback
subscriber.connect('localhost')
subscriber.subscribe('iotevents/+/#')

try:
    subscriber.loop_forever()
except KeyboardInterrupt:
    pass
```

```console
$ python3 subscriber.py
topic: temperature/X002, msg:
{
 'identifier': 'X002',
 'value': 36, 'unit':
 'Celsius',
 'timestamp': 1668347911.566947
} 36
```

> Pueden ejecutarse varios (¡aconsejable para probar!)

## Sistemas de colas de mensajes

Mientras que los grupos y la publicación-suscripción brindan un estilo de comunicación _uno-a-muchos_, las colas de mensajes brindan un servicio punto-a-punto utilizando el concepto de cola de mensajes como dirección indirecta, logrando así las propiedades deseadas de <ins>desacoplamiento</ins> de espacio y tiempo.

Son _punto-a-punto_ en el sentido de que el remitente coloca el mensaje en una cola y luego el destinatario lo elimina mediante un **único** proceso.

### RabbitMQ

Implementa el estándar AMQP (Advanced Message Queuing Protocol):
- **Publicadores**: enviar mensajes a un intercambio
- **Intercambios**: implementar enrutamiento para enviar mensajes a los consumidores.
- **Consumidores**: declaran la cola y la vinculan a un intercambio para recibir mensajes.
- **Colas**: almacenar temporalmente mensajes de publicadores
- **Enrutamiento**: aplique claves de enrutamiento para realizar la coincidencia de mensajes: intercambios directos, en abanico y de temas.