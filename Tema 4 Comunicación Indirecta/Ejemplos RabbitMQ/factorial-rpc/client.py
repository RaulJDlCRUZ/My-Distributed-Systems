#!/usr/bin/python3

import pika
import uuid
import sys


class FactorialRpcClient(object):
    def __init__(self):
        localhost = pika.ConnectionParameters(host='localhost')
        self.connection = pika.BlockingConnection(localhost)
        self.channel = self.connection.channel()
        # Envía una solicitud RPC y se bloquea hasta que se recibe la respuesta
        # Es una cola exclusiva y anónima, sólo una/cliente
        result = self.channel.queue_declare(queue='', exclusive=True)
        self.callback_queue = result.method.queue

        self.channel.basic_consume(
            on_message_callback=self.on_response,  # comprobación de id igual
            auto_ack=False,  # Desactivamos ACK automáticos
            queue=self.callback_queue
        )

    def on_response(self, ch, method, props, body):
        # *Justo aquí se comprueba que el id de correlación sea igual, para poder romper con el ciclo de consumo
        if self.corr_id == props.correlation_id:
            self.response = body

    def call(self, n):
        # Envía una solicitud RPC y se bloquea hasta que se recibe la respuesta
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(
            exchange='',
            routing_key='rpc_queue',
            body=str(n),
            properties=pika.BasicProperties(
                # Se usa comúnmente para nombrar una cola de devolución de llamadas.
                reply_to=self.callback_queue,
                # Útil para correlacionar respuestas RPC con solicitudes (TIENE QUE SER IGUAL!!*)
                correlation_id=self.corr_id,
            )
        )

        while self.response is None:
            self.connection.process_data_events()

        return int(self.response)


if len(sys.argv) < 2:
    print(f"Usage: {sys.argv[0]} [int] (10 max)")
    sys.exit(1)

if not sys.argv[1].isdigit() or int(sys.argv[1]) > 10:
    print(" [!] Please provide an integer as argument, 10 max")
    sys.exit(1)

client = FactorialRpcClient()

print(" [x] Requesting factorial(%d)" % int(sys.argv[1]))
response = client.call(int(sys.argv[1]))
print(" [.] Got %r" % response)
