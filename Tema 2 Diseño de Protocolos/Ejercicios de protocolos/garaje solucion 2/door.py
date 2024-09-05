#!/usr/bin/python3

import socket
from door_pb2 import ControlMessage, ResponseMessage

class Door:
    CLOSED = ResponseMessage.ALREADY_CLOSED
    OPEN = ResponseMessage.ALREADY_OPEN

    def __init__(self):
        self.status = Door.CLOSED

    def open(self, mode, time):
        if self.status == Door.OPEN:
            print(f'[!] Door already open.')
            return ResponseMessage.ALREADY_OPEN

        # Implement something for random errors and time
        self.status = Door.OPEN
        print(f'[-] Door opened. Mode: {mode}. Time: {time}')
        return ResponseMessage.OK

    def close(self):
        if self.status == Door.CLOSED:
            print(f'[!] Door already closed.')
            return ResponseMessage.ALREADY_CLOSED

        # Implement something for random errors
        self.status = Door.CLOSED
        print('[-] Door closed.')
        return ResponseMessage.OK


def handle_client(client_socket, door):
    request_data = client_socket.recv(1024)
    control_msg = ControlMessage()
    control_msg.ParseFromString(request_data)

    response = ResponseMessage()
    response.id = control_msg.id

    if control_msg.command == ControlMessage.CHECK_STATUS:
        response.result = door.status

    if control_msg.command == ControlMessage.OPEN:
        response.result = door.open(control_msg.mode, control_msg.time)

    if control_msg.command == ControlMessage.CLOSE:
        response.result = door.close()

    client_socket.send(response.SerializeToString())
    client_socket.close()


if __name__ == "__main__":
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('', 9999))
    server.listen(5)
    print('Server listening on port 9999')

    door = Door()

    while True:
        client_socket, addr = server.accept()
        handle_client(client_socket, door)