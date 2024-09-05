#!/usr/bin/python3
# Adapted from: https://www.rabbitmq.com/tutorials/tutorial-five-python.html
#   as receive_logs_topic.py

import sys
import pika


def callback(ch, method, properties, body):
    print("[x] Received %r: %r " % (method.routing_key, body.decode("UTF-8")))


'''
Importante sobre TOPIC: Mensaje no puede ser una clave arbitraria:
-> Ha de ser una lista de palabras separadas por puntos <*.*...> -> max 255 bytes
Digamos que es como el binding directo, pero va como los topics de mqtt:
    - '*' -> Sustituye una palabra
    - '#' -> Sustituye 0 o muchas palabras (hasta el final)
'''

localhost = pika.ConnectionParameters(host='localhost')
connection = pika.BlockingConnection(localhost)
channel = connection.channel()

channel.exchange_declare(exchange='twitter-pattern', exchange_type='topic')
result = channel.queue_declare(queue='', exclusive='True')
queue_name = result.method.queue

binding_keys = sys.argv[1:]
if not binding_keys:
    sys.stderr.write("Usage: {} [binding key]...\n".format(sys.argv[0]))
    sys.exit(1)

for binding_key in binding_keys:
    # Vamos a crear un nuevo enlace para cada 'topic' o key que nos interese. Antes era uno solo
    channel.queue_bind(
        exchange='twitter-pattern',
        queue=queue_name,
        routing_key=binding_key  # Si fuera fanout, esto se ignora
    )

channel.basic_consume(
    on_message_callback=callback,
    queue=queue_name,
    auto_ack=True
)

print('[*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
