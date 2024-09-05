#!/usr/bin/python3
# Adapted from: https://www.rabbitmq.com/tutorials/tutorial-five-python.html
#   as emit_log_topic.py (almost same as tutorial 4)

import sys
import pika

localhost = pika.ConnectionParameters(host='localhost')
connection = pika.BlockingConnection(localhost)
channel = connection.channel()

channel.exchange_declare(exchange='twitter-pattern', exchange_type='topic')
routing_key = sys.argv[1] if len(sys.argv) > 2 else 'anonymous.info'

message = ' '.join(sys.argv[2:]) or "Hello world!"

channel.basic_publish(
    exchange='twitter-pattern',
    routing_key=routing_key,
    body=message
)

print("[x] Sent %r:%r: " % (routing_key, message))
connection.close()
