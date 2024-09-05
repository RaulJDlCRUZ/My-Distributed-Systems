#!/usr/bin/python3

import pika


class App:
    def __init__(self, broker_host):
        self.broker_host = 'FILL'

        credentials = pika.PlainCredentials('ssdd', 'student')
        self.parameters = pika.ConnectionParameters(
            host=broker_host,
            credentials=credentials
        )

        self.get_code()

    def get_code(self):
        self.code_connection = pika.BlockingConnection(self.parameters)

    def callback(self, ch, method, props, body):
        self.code_connection.close()
