#Autor = Raúl Jiménez de la Cruz

import pika

NAME = "RAÚL JIMÉNEZ DE LA CRUZ"
DNI = "X-01234567"

# _HOST = '192.168.8.224'
_HOST = 'localhost'


def callback(ch, method, properties, body):
    connection.close()
    print("[x] Received: %r" % body.decode("UTF-8"))
    m1 = f'{body.decode("UTF-8")} {NAME} {DNI}' #Code Name DNI
    print(m1)
    # Publicar exchange en modo publicación suscripción, routing key en las propiedades del mensaje
    return_connection=pika.BlockingConnection(pika.ConnectionParameters(host=_HOST))
    return_channel=return_connection.channel()

    return_channel.exchange_declare(exchange='results', exchange_type='topic')
    result_2 = return_channel.queue_declare(queue='', exclusive='False')

    return_channel.queue_bind(exchange='results', queue=result_2.method.queue, routing_key=properties.reply_to)
    
    return_channel.basic_publish(
    exchange='results',
    routing_key=properties.reply_to,
    body=m1
    )
    
    print('[!] Enviado: ',m1)
    

# credentials = pika.PlainCredentials('ssdd', 'student')
parameters = pika.ConnectionParameters(
            host=_HOST,
            # credentials=credentials
        )
connection = pika.BlockingConnection(parameters)

channel = connection.channel()
result = channel.queue_declare(queue='codes')

channel.basic_consume(
    queue='codes',
    auto_ack=True,
    on_message_callback=callback,
)

print("[*] Waiting for messages. press Ctrl+C to exit")
channel.start_consuming()