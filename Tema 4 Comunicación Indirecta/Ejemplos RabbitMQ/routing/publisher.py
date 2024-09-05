#!/usr/bin/env python
# Extracted from: https://www.rabbitmq.com/tutorials/tutorial-four-python.html
#   as emit_log_direct.py

import pika
import sys

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='direct_logs', exchange_type='direct') # Crear intercambio directo

severity = sys.argv[1] if len(sys.argv) > 1 else 'info'
message = ' '.join(sys.argv[2:]) or 'Hello World!'
# Enviar mensaje
channel.basic_publish(
    exchange='direct_logs', routing_key=severity, body=message)
print(" [x] Sent %r:%r" % (severity, message))
# Se asume que severity puede ser de 'info', 'warning' o 'error'
connection.close()
