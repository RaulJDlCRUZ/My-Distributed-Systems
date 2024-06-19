## The struct module

### ES

Implementar un script servidor y un script cliente que hagan lo siguiente (con sockets UDP):

- Cliente: envía un mensaje al servidor consistente en un entero de 16 bits y una cadena aleatoria.
        El número entero indica la longitud de la cadena.
- Servidor: recibe el mensaje del cliente, lo decodifica y lo muestra en pantalla.

Tenga en cuenta que la longitud de la cadena es variable, por lo que el servidor debe descodificar el mensaje dinámicamente.

### EN

Implement a server script and a client script that do the following (with UDP sockets):

- Client: send a message to the server consisting of a 16-bit integer and a random string.
        The integer indicates the length of the string.
- Server: receive the message from the client, decode it, and display it on the screen.

Keep in mind that the length of the string is variable, so the server must decode the message dynamically.

**[`lorem.txt`](lorem.txt) para probar texto de ejemplo**