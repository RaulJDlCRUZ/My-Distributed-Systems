#!/usr/bin/python3

import json
import time
import paho.mqtt.client as mqtt

from videogames import deals


def build_event(videogame):
    return {
        "name": videogame["name"],
        "discount": videogame["discount"],
    }


publisher = mqtt.Client()
publisher.connect('127.0.0.1')

print('Publishing videogame deals')

for i in deals:
    videogame_info = f'videogames/deals/{i["type"].lower()}/{i["developer"].lower()}'
    publisher.publish(videogame_info, json.dumps(build_event(i)))
    print('.', end='', flush=True)  # No \n !
    time.sleep(1)

publisher.disconnect()
