#!/usr/bin/python3
# Adapted from: https://www.rabbitmq.com/tutorials/tutorial-three-python.html
#   as receive_logs.py

import pika


def callback(ch, method, properties, body):
	print("[x] Received %r " % (body.decode("UTF-8")))


localhost = pika.ConnectionParameters(host='localhost')
connection = pika.BlockingConnection(localhost)
channel = connection.channel()

channel.exchange_declare(exchange='twitter', exchange_type='fanout')
# Cola fresca y vacía. Se destruirá al cerrar la conexión -> Exclusive = True
result = channel.queue_declare(queue='', exclusive='True')
# Contiene un nombre ALEATORIO de cola de mensajes
queue_name = result.method.queue
# Ya hemos creado un intercambio fanout y una cola. Ahora necesitamos decirle al intercambio que envíe mensajes a nuestra cola.
# Esa relación o atadura entre el intercambio y una cola se llama enlace (=binding).
channel.queue_bind(exchange='twitter', queue=queue_name)

channel.basic_consume(
	on_message_callback=callback,
	queue=queue_name,
	auto_ack=True
)

print("[*] Waiting for messages. To exit press Ctrl+")
channel.start_consuming()
