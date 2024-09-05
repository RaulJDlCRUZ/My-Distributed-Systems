#!/usr/bin/python3
# Extracted from: https://www.rabbitmq.com/tutorials/tutorial-two-python.html

import sys
import pika


localhost = pika.ConnectionParameters(host='localhost')
connection = pika.BlockingConnection(localhost)
channel = connection.channel()
# Cola duradera: si RabbitMQ falla, no se perderán las tareas (LA COLA NO DESAPARECE)
channel.queue_declare(queue='task_queue', durable=True)

for msg in sys.argv[1:]:
    channel.basic_publish(
        exchange='',
        routing_key='task_queue', # Igual que en 1, no hay exchange, hay una 'dirección' a una cola en concreto
        body=msg,
        # La siguiente propiedad permite que los MENSAJES no se pierdan
        properties=pika.BasicProperties(
            delivery_mode=2  # make message persistent === pika.spec.PERSISTENT_DELIVERY_MODE
        ))
# De forma predeterminada, RabbitMQ enviará cada mensaje al siguiente consumidor, en secuencia.
# En promedio, todos los consumidores recibirán la misma cantidad de mensajes.
#! Esta forma de distribuir mensajes se llama ROUND-ROBIN
    print(f'[x] Sent: {msg}')

connection.close()
