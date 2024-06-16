## The struct module
Implement a server script and a client script that do the following (with UDP sockets):

- Client: send a message to the server consisting of a 16-bit integer and a random string.
        The integer indicates the length of the string.
- Server: receive the message from the client, decode it, and display it on the screen.

Keep in mind that the length of the string is variable, so the server must decode the message dynamically.
