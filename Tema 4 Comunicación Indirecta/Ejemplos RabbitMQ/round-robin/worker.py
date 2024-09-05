#!/usr/bin/python3
# Extracted from: https://www.rabbitmq.com/tutorials/tutorial-two-python.html

import time
import pika
#! USO DE COLA DE TAREAS PARA REPARTIR EL TRABAJO!

STRICT_ROUND_ROBIN = True

def callback(ch, method, properties, body):
    print("[x] Received %r " % (body.decode("UTF-8")))
    # Simulamos que estamos ocupados (espera en función de '.' en argv[1:]), pero esto no sirve para nada:
    time.sleep(body.count(b'.'))
    print("[x] Done")
    # Para garantizar que un mensaje nunca se pierda, RabbitMQ admite acuses de recibo de mensajes.
    # El consumidor envía un acuse de recibo (recibo) para decirle a RabbitMQ que se recibió,
    # procesó un mensaje en particular y que RabbitMQ es libre de eliminarlo.
    #! AHORA SI NO LLEGA UN ACK, PRODUCTOR ENTIENDE QUE NO SE PROCESÓ BIEN -> LO VUELVE A ENCOLAR (30 min timeout)
    #* Por ello, quitamos la flag en el canal y hacemos un ack expresamente en el callback:
    ch.basic_ack(delivery_tag=method.delivery_tag)


localhost = pika.ConnectionParameters(host='localhost')
connection = pika.BlockingConnection(localhost)
channel = connection.channel()
# Cola duradera: si RabbitMQ falla, no se perderán las tareas (LA COLA NO DESAPARECE)
channel.queue_declare(queue='task_queue', durable=True)

'''
Dispatch Justo:
Hasta ahora RabbitMQ simplemente envía un mensaje cuando el mensaje ingresa a la cola.
No analiza la cantidad de mensajes no reconocidos de un consumidor.
Simplemente envía ciegamente cada enésimo mensaje al enésimo consumidor.

'''
if STRICT_ROUND_ROBIN:
    # Se limita a aplicar Round-Robin con su problemática
    channel.basic_qos()
else:
    # Indica a RabbitMQ que no dé más de un mensaje a un trabajador a la vez
    #! => no envíe un nuevo mensaje a un trabajador hasta que haya procesado y reconocido el anterior.
    channel.basic_qos(prefetch_count=1)

channel.basic_consume(
    on_message_callback=callback,
    queue='task_queue'
)

print("[*] Waiting for messages. Press Ctrl+C to exit")
channel.start_consuming()
