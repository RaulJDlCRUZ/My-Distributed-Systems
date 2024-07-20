CREDENCIALES
===========

Para conectarse a un _broker_ remoto use las credenciales de nombre de usuario "ssdd" y contraseña "student" mediante este código:

```python
credentials = pika.PlainCredentials('ssdd', 'student')
parameters = pika.ConnectionParameters(host=<RabbitMQ-server>, credentials=credentials)
connection = pika.BlockingConnection(parameters)
```


DIAGRAMA DE FLUJO
============

```
STUDENT				BROKER                          PROFESSOR
|                                                           |
| connection()                                              |
| queue_name: "codes"                                       |
| <------------------------- |1|2|3| | | |  <-------------- |
|                                                           |
|                                                           |
| connection() style PUBLISH-SUBSCRIBE                      |
| exchange: "results"                                       |
| routing_key: message props                                |
|  	       	                                                |
| ------------> EXCHANGE ---> | | | | |m1| ---------------> |
|                   m1="Code Name DNI"                      |
```

## Material proporcionado

### Esqueleto de estudiante [`student-skel.py`](student-skel.py)

```python
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
```

### [`teacher`](teacher.py)

```python
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
```