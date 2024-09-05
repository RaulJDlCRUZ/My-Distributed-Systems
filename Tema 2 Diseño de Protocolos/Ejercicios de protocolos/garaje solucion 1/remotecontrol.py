#!/usr/bin/python3
import socket
import argparse
# Voy a importar del protocolbuffer2 mis variables del .proto
from door_pb2 import RemoteControl, DoorSensor
MSG_ID = 1  # Id de mensaje macro. Posible contador?
class Controller:
    # Método constructor
    def __init__(self, server_ip, server_port):
        self.server_ip = server_ip
        self.server_port = server_port
    # Método de envío del mensaje
    def send_message(self, msg):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((self.server_ip, self.server_port))

        # Serializa el mensaje y lo devuelve como una cadena
        # ...después se envía al sensor y se espera su respuesta
        client_socket.send(msg.SerializeToString())
        response_data = client_socket.recv(1024)

        # Se parsea la respuesta recibida del sensor de la puerta
        _door_response = DoorSensor()
        _door_response.ParseFromString(response_data)

        client_socket.close()
        # Devolvemos la respuesta
        return _door_response 
    # Métodos de las acciones primitivas del control remoto
    def open_door(self, mode=RemoteControl.VEHICLE, time=None):
        # 0) Abrir puerta. Además de los atributos constructor, añadimos modo y tiempo
        # Primero, creo la variable del mando remoto para la puerta:
        opn_msg = RemoteControl()
        # Rellenar campos de dicho mensaje de nuestro protocolo
        opn_msg.id = MSG_ID
        opn_msg.cmnd = RemoteControl.OPEN
        opn_msg.time = time
        opn_msg.mode = RemoteControl.WALKER if mode == 'walker' else RemoteControl.VEHICLE

        # Luego, envío el mensaje:
        reply = self.send_message(opn_msg)

        # Devolvemos la respuesta:
        return reply.response, reply.state
    def close_door(self):
        # 1) Cerrar puerta.
        cls_msg = RemoteControl()
        cls_msg.id = MSG_ID
        cls_msg.cmnd = RemoteControl.CLOSE
        reply = self.send_message(cls_msg)
        return reply.response, reply.state
    def check_status(self):
        # 2) Comprobar estado de la puerta
        chk_msg = RemoteControl()
        chk_msg.id = MSG_ID
        chk_msg.cmnd = RemoteControl.CHECK_STATUS
        reply = self.send_message(chk_msg)
        return reply.state

# Parser de argumentos
parser = argparse.ArgumentParser(description='Door Controller')
parser.add_argument('-s', '--server', type=str, default='localhost', help='Server IP Address')

command_subparsers = parser.add_subparsers(dest='command', help='Commands', metavar='COMMAND')

# COMANDO 1:
open_parser = command_subparsers.add_parser('open', help='Open door')
#   Argumentos opcionales para OPEN
open_parser.add_argument('-t', '--time', type=int, default=0, help='Time to keep the door open in seconds')
open_parser.add_argument('-m', '--mode', choices=['vehicle', 'walker'], default='vehicle', help='Mode to open the door')

# COMANDO 2:
close_parser = command_subparsers.add_parser('close', help='Close door')
# COMANDO 3:
check_parser = command_subparsers.add_parser('status', help='Check door status')

if __name__ == "__main__":
    args = parser.parse_args()
    if args.command is None:
        parser.print_help()
        exit(1)
    else:
        PORT = 9997
        controller = Controller(args.server, PORT)
        final_result = ''
        if args.command == 'open':
            response,state = controller.open_door(args.mode, args.time)
            final_result+=f'Result: {response} '

        if args.command == 'close':
            response,state = controller.close_door()
            final_result+=f'Result: {response} ' 
            
        
        if args.command == 'status':
            state = controller.check_status()
        
        final_result+=f'State: {state} (check spec to know the meaning)'
        print(final_result)

