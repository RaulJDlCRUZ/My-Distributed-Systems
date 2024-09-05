#!/usr/bin/python3

import pika


localhost = pika.ConnectionParameters(host='localhost')
connection = pika.BlockingConnection(localhost)
channel = connection.channel()
# Borra la que existiera con anterioridad
channel.queue_delete(queue='rpc_queue')
# Se vuelve a declarar
channel.queue_declare(queue='rpc_queue')


def factorial(n):
    return 1 if n == 0 else n * factorial(n - 1)


def on_request(ch, method, props, body):
    n = int(body)

    print(" [.] factorial(%s)" % n)
    response = factorial(n)
    # Definición de propiedades. Se establece el correlation_id para que sea el mismo a cliente
    properties = pika.BasicProperties(
        correlation_id=props.correlation_id
    )
    # Publicación por el canal.
    ch.basic_publish(
        exchange='',
        routing_key=props.reply_to,
        properties=properties,
        body=str(response)
    )
    # Envío manual de ack
    ch.basic_ack(delivery_tag=method.delivery_tag)


# Si queremos más servidores y distribuir la carga por igual, debemos establecer la configuración prefetch_count.
channel.basic_qos(prefetch_count=1)
channel.basic_consume(
    on_message_callback=on_request,
    queue='rpc_queue'
)

print(" [x] Awaiting RPC requests")
channel.start_consuming()
