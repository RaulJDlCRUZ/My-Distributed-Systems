## Basic Sockets
Implement a server script and a client script that do the following (with UDP sockets):

1. The server must listen on an accessible port.
2. The client must send a message to the server.
3. The server must decode the message and display it on the screen.

Things to consider:

- The client's message must be encoded in utf-8.
- The server must decode the message in ascii.
- Due to the difference in encodings, the server must somehow handle decoding errors.

Try to
    1) test by sending the string "ñandú" from the client to see the decoding errors, and
    2) run the exercise with another person (each of you runs one script, either the client or the server).
