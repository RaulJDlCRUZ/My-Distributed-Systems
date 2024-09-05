#!/usr/bin/python3
# Adapted from: https://www.rabbitmq.com/tutorials/tutorial-three-python.html
#   as emit_log.py

import sys
import pika

localhost = pika.ConnectionParameters(host='localhost')
connection=pika.BlockingConnection(localhost)
channel=connection.channel()

# Declaración del exchange del canal:
#  - Direct:  Usa una clave de enrutamiento de mensajes para transportarlos a las colas
#  - Topic:   Envía mensajes dependiendo de las coincidencias de comodines entre la clave de
#             enrutamiento y el patrón de enrutamiento del enlace de cola.
#  - Fanout:  Duplica y enruta un mensaje recibido a cualquier cola asociada, independientemente
#             de las claves de enrutamiento o la coincidencia de patrones. Aquí, las CLAVES PROPORCIONADAS
#             SERÁN COMPLETAMENTE IGNORADAS*. Algo asó como un BROADCAST
#  - Headers: Sistema de enrutamiento de mensajes que utiliza argumentos con encabezados y
#             valores opcionales para enrutar mensajes.

channel.exchange_declare(exchange='twitter', exchange_type='fanout')

message=' '.join(sys.argv[1:]) or "Hello world!"

channel.basic_publish(
    exchange='twitter', # Establezco el nombre del intercambio o exchange COMPARTIDO
    routing_key='',     #* no se proporciona ninguna clave de enrutado, pues en fanout se ignoran/no necesito saberla
    body=message
)

print("[x] Sent: ", message)
connection.close()
