#!/usr/bin/env python
# Extracted from: https://www.rabbitmq.com/tutorials/tutorial-two-python.html
#   as new_task.py

import pika
import sys

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='task_queue', durable=True) # Durable=True para asegurarse de que los mensajes no se pierdan incluso si RabbitMQ se apaga.

# Permitir el envío de mensajes arbitrarios desde la línea de comando. Este programa programará tareas en nuestra cola de trabajos.
message = ' '.join(sys.argv[1:]) or "Hello World!"
channel.basic_publish(
    exchange='',
    routing_key='task_queue',
    body=message,
    properties=pika.BasicProperties(
        delivery_mode=2,  # make message persistent
    ))
print(" [x] Sent %r" % message)
connection.close()
