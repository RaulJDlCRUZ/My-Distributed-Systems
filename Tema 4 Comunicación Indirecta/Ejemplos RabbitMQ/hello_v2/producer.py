#!/usr/bin/python3
# Adapted from: https://www.rabbitmq.com/tutorials/tutorial-one-python.html

import pika  # Implementación AMPQ
import time

# Nueva instancia de conexión AMPQ
localhost = pika.ConnectionParameters(host='localhost')
# Conexión nueva con métodos que se bloquearán hasta que haya regresado la respuesta esperada desde el host. Es TCP!
connection = pika.BlockingConnection(localhost)
# Creación de un canal = conexión virtual!
channel = connection.channel()
# Especificación (creación si es necesario) de la cola del canal de la conexión.
'''Nota: debemos asegurarnos de que exista la cola de destinatarios.
Si enviamos un mensaje a una ubicación que no existe, RabbitMQ simplemente dejará caer el mensaje.'''
channel.queue_declare(queue="hello")

message = "Hello world! {}".format(time.time())

# Publicación al canal un mensaje. El mensaje puede contener el intercambio,
channel.basic_publish(
    # Intercambio. Recibe mensajes de productores y los empuja a la queue. Nombre '' = el default
    exchange='',
    routing_key='hello',    # Clave de enrutado. Clave que mira el exchange para decidir cómo enrutar los mensajes a las colas. Es una "address"
    # Cuerpo del mensaje. El contenido en cuestión. En este caso es un Hola Mundo con el tiempo del sistema.
    body=message
)

#! Este intercambio es especial: nos permite especificar exactamente a qué cola debe ir el mensaje -> su nombre en route_key

print("[x] Sent: ", message)
connection.close()  # Buffers se limpian, mensaje enviado a RabbitMQ y cierre de conexión
