from http.server import HTTPServer, SimpleHTTPRequestHandler

server = HTTPServer(('', 8000), SimpleHTTPRequestHandler)
# Como sockname() devuelve una tupla IP-Puerto, lo aprovechamos para abreviar el formato
print("Open http://{}:{}".format(*server.socket.getsockname()))
# Excepción para manejar el Control+C de cerrado
try:
    server.serve_forever()
except KeyboardInterrupt:
    server.server_close()
