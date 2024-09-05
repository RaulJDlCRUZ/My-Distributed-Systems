#!/usr/bin/python3
# Adapted from: https://www.rabbitmq.com/tutorials/tutorial-one-python.html

import pika


def callback(ch, method, properties, body):
    '''Cada vez que recibimos un mensaje, la biblioteca Pika llama a esta función de devolución de llamada.
    En nuestro caso esta función imprimirá en pantalla el contenido del mensaje.'''
    print("[x] Received: %r" % body.decode("UTF-8"))


# Similar al productor. Consumidor define parámetros de conexión, el tipo de conexión (bloqueante) y el canal
localhost = pika.ConnectionParameters('localhost')
connection = pika.BlockingConnection(localhost)
channel = connection.channel()
# Declaración de la cola de mensajes del canal
channel.queue_declare(queue='hello')

channel.basic_consume(
    # Nombre de la cola a consumir (creada anteriormente con queue_declare)
    queue='hello',
    auto_ack=True,                  # Acknowledgement automático
    on_message_callback=callback,   # Método de redirección para cuando llega un mensaje
)

print("[*] Waiting for messages. press Ctrl+C to exit")
# Método bloqueante que estará consumiendo desde la cola de mensajes
channel.start_consuming()
