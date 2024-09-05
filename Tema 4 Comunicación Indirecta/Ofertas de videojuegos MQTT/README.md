# Videogame deals notifier

## ES

En este ejercicio debes crear un sistema de notificación de ofertas de videojuegos utilizando el protocolo MQTT en Python, con el módulo `Paho`. El sistema constará de dos partes: un publicador que enviará información sobre ofertas de videojuegos, y un suscriptor que recibirá dichas notificaciones en función de los intereses del usuario.

El editor deberá enviar mensajes con el nombre del videojuego y el porcentaje de descuento, uno por segundo, a un broker MQTT según la jerarquía de tópicos (_topics_):

```console
videogames/deals/<type>/<developer>
```

El suscriptor debe suscribirse a temas según los intereses del usuario, que se especificarán a través de la línea de comandos. Por ejemplo, si el usuario está interesado en videojuegos de acción de los desarrolladores Ubisoft y Rockstar:

```console
subscriber.py -d ubisoft rockstar -t action
```

Y si están interesados en cualquier tipo de videojuego del desarrollador Valve:

```console
subscriber.py -d valve
```

Para todos los mensajes de interés, se publicará un texto en el terminal, imprimiendo un texto especial en caso de que el descuento sea superior al 70%.

## EN

In this exercise, you are to create a videogame deals notification system using the MQTT protocol in Python, with the Paho module. The system will consist of two parts: a publisher that will send out information about videogame deals, and a subscriber that will receive such notifications according to the user's interests.

The publisher should send messages with the name of the videogame and the discount percentage, one per second, to an MQTT broker according to the topic hierarchy:

```
videogames/deals/<type>/<developer>
```

The subscriber should subscribe to topics according to the user's interests, which will be specified via command line. For example, if the user is interested in action videogames from the developers Ubisoft and Rockstar:

```
subscriber.py -d ubisoft rockstar -t action
```

And if they are interested in any type of videogame from the developer Valve:

```
subscriber.py -d valve
```

For all messages of interest, a text will be published on the terminal, printing a special text in case the discount is greater than 70%.