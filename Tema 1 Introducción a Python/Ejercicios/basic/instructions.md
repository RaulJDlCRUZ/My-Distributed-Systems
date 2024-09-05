## Basic Sockets

### ES

Implementar un script servidor y un script cliente que hagan lo siguiente (con sockets UDP):

1. El servidor debe escuchar en un puerto accesible.
2. El cliente debe enviar un mensaje al servidor.
3. El servidor debe decodificar el mensaje y mostrarlo en la pantalla.

Aspectos a tener en cuenta:

- El mensaje del cliente debe estar codificado en utf-8.
- El servidor debe decodificar el mensaje en ascii.
- Debido a la diferencia en las codificaciones, el servidor debe manejar de alguna manera los errores de decodificación.

Intente<br>
&emsp;1) hacer una prueba enviando la cadena "ñandú" desde el cliente para ver los errores de descodificación, y<br>
&emsp;2) ejecutar el ejercicio con otra persona (cada uno ejecuta un script, ya sea el cliente o el servidor).

### EN

Implement a server script and a client script that do the following (with UDP sockets):

1. The server must listen on an accessible port.
2. The client must send a message to the server.
3. The server must decode the message and display it on the screen.

Things to consider:

- The client's message must be encoded in utf-8.
- The server must decode the message in ascii.
- Due to the difference in encodings, the server must somehow handle decoding errors.

Try to<br>
&emsp;1) test by sending the string "ñandú" from the client to see the decoding errors, and<br>
&emsp;2) run the exercise with another person (each of you runs one script, either the client or the server).
