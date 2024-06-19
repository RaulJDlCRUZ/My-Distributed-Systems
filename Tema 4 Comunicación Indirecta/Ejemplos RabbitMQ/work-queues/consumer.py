#!/usr/bin/env python
# Extracted from: https://www.rabbitmq.com/tutorials/tutorial-two-python.html
#   as worker.py

import pika
import time

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='task_queue', durable=True) # Durable=True para asegurarse de que los mensajes no se pierdan incluso si RabbitMQ se apaga.
print(' [*] Waiting for messages. To exit press CTRL+C')


def callback(ch, method, properties, body):
    print(" [x] Received %r" % body.decode())
    # necesita fingir un segundo de trabajo por cada punto en el cuerpo del mensaje. Extraerá mensajes de la cola y realizará la tarea.
    time.sleep(body.count(b'.'))
    print(" [x] Done")
    # Enviar un ACK adecuado por parte del worker, una vez que hayamos terminado con una tarea.
    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_qos(prefetch_count=1) # No enviar un nuevo mensaje al worker hasta que haya procesado y enviado un ACK para el anterior. (no más de 1 a la vez!)
channel.basic_consume(queue='task_queue', on_message_callback=callback)

channel.start_consuming()
