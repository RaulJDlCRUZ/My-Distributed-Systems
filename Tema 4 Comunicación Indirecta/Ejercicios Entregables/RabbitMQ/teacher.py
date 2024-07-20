#!/usr/bin/python3

import pika
import uuid

KEY = 'students.results'


class App:
    def __init__(self):
        self.parameters = pika.ConnectionParameters(host='localhost')
        self.codes = []

    def init_codes_queue(self):
        connectionCodes = pika.BlockingConnection(self.parameters)
        self.channelCodes = connectionCodes.channel()
        self.channelCodes.queue_delete(queue="codes")
        self.channelCodes.queue_declare(queue="codes", durable=False)

        for _ in range(200):
            self.send_code(str(uuid.uuid4()))

    def send_code(self, code):
        self.channelCodes.basic_publish(
            exchange='',
            routing_key='codes',
            body=code,
            properties=pika.BasicProperties(
                reply_to=KEY,
            )
        )

        self.codes.append(code)
        print("[x] Sent: ", code)

    def wait_for_messages(self):
        connectionStudents = pika.BlockingConnection(self.parameters)
        channelStudents = connectionStudents.channel()
        channelStudents.exchange_declare(exchange='results', exchange_type='topic')
        result = channelStudents.queue_declare(queue='', exclusive='False')
        queue_name = result.method.queue

        channelStudents.queue_bind(exchange='results', queue=queue_name, routing_key=KEY)
        print("[*] Waiting for messages. To exit press Ctrl+C")
        channelStudents.basic_consume(on_message_callback=self.callback, queue=queue_name)
        channelStudents.start_consuming()

    def callback(self, ch, method, properties, body):
        message = body.decode("UTF-8")
        code = message.split()[0]

        if code not in self.codes:
            print("[*] Received code {} does NOT exist".format(code))
            return

        self.codes.remove(code)
        print(f"[x] Received code {code}")
        self.send_code(str(uuid.uuid4()))


app = App()
app.init_codes_queue()
app.wait_for_messages()
