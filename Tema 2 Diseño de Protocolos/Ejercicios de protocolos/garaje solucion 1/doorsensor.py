#!/usr/bin/python3
import socket
# Voy a importar del protocolbuffer2 mis variables del .proto
from door_pb2 import RemoteControl, DoorSensor

class Door:
    # Tomamos los estados del .proto para crear el objeto
    CLOSED = DoorSensor.ALREADY_CLOSE
    OPEN = DoorSensor.ALREADY_OPEN
    
    def __init__(self):
        self.status = Door.CLOSED # Presuponemos que inicialmente está cerrada
    
    def open(self, mode, time):
        # ABRIR LA PUERTA
        if self.status == Door.OPEN:
            print(f'[!] Door already open.')
            return DoorSensor.ERROR, self.status

        # Una vez controlado si la puerta estaba abierta...
        self.status = Door.OPEN
        print(f'[-] Door opened. Mode: {mode}. Time: {time}')
        return DoorSensor.ACK, self.status
    
    def close(self):
        # CERRAR LA PUERTA
        if self.status == Door.CLOSED:
            print(f'[!] Door already closed.')
            return DoorSensor.ERROR, self.status

        # Una vez controlado si la puerta estaba cerrada...
        self.status = Door.CLOSED
        print('[-] Door closed.')
        return DoorSensor.ACK, self.status

def handle_client(client_socket, door):
    # Para manejar a un cliente, primero debe llegar un mensaje:
    request_data = client_socket.recv(1024)
    # Nueva variable del control remoto (lo que nos llegue, debemos parsearlo)
    control_msg = RemoteControl()
    control_msg.ParseFromString(request_data)
    # Creamos la respuesta, nueva variable sensor de puerta
    response = DoorSensor()
    #   ID
    response.id = control_msg.id
    #   RESPUESTA DEL SENSOR Y ESTADO DE LA PUERTA
    if control_msg.cmnd == RemoteControl.CHECK_STATUS:
        response.state = door.status

    if control_msg.cmnd == RemoteControl.OPEN:
        response.response, response.state = door.open(control_msg.mode, control_msg.time)

    if control_msg.cmnd == RemoteControl.CLOSE:
        response.response, response.state = door.close()

    client_socket.send(response.SerializeToString())
    client_socket.close()

if __name__ == "__main__":
    try:    
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        PORT = 9997
        server.bind(('', PORT))
        server.listen(5)
        print(f'Server listening on port {PORT}')

        door = Door()

        while True:
            client_socket, addr = server.accept()
            handle_client(client_socket, door)
    except KeyboardInterrupt:
        pass