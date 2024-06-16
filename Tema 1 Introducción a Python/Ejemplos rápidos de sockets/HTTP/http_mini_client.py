import socket

s = socket.socket()
s.connect(('insecure.org', 80))
s.send(b"GET /\n")
print(s.recv(2048))
