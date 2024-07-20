#!/usr/bin/python3
# -*- coding: utf-8; mode: python -*-
# IP: 192.168.8.224
# Puerto 1883
import json
import paho.mqtt.client as mqtt
# Autor = Raúl Jiménez de la Cruz
def take_reading(decoded):
    return {
  'code': str(decoded),
  'fullname': 'Raúl Jiménez de la Cruz',
  'dni': '01234567'
}

def callback(client, userdata, message):
    decoded = json.loads(message.payload.decode())
    # print("topic: {}",message.topic)
    print("Código a enviar: ",decoded)
    # print(take_reading(decoded))
    publisher = mqtt.Client()
    publisher.connect('192.168.8.224')
    publisher.publish('ssdd/ejercicio004/person/result',json.dumps(take_reading(decoded)))


# Suscriptor del código
subscriber = mqtt.Client()
subscriber.on_message = callback
subscriber.connect('192.168.8.224')
subscriber.subscribe('ssdd/ejercicio004/person/code')


try:
    subscriber.loop_forever()
except KeyboardInterrupt:
    pass


