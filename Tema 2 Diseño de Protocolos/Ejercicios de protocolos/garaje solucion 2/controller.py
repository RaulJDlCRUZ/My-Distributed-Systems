#!/usr/bin/python3

import socket
import argparse
from door_pb2 import ControlMessage, ResponseMessage

MSG_ID = 1  # You can make this dynamic or based on some counter

class Controller:
    def __init__(self, server_ip, server_port):
        self.server_ip = server_ip
        self.server_port = server_port

    def send_message(self, msg):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((self.server_ip, self.server_port))

        client_socket.send(msg.SerializeToString())

        response_data = client_socket.recv(1024)
        response = ResponseMessage()
        response.ParseFromString(response_data)

        client_socket.close()
        return response

    def check_status(self):
        msg = ControlMessage()
        msg.id = MSG_ID
        msg.command = ControlMessage.CHECK_STATUS

        response = self.send_message(msg)
        return response.result

    def open_door(self, mode=ControlMessage.VEHICLE, time=None):
        msg = ControlMessage()
        msg.id = MSG_ID
        msg.command = ControlMessage.OPEN
        msg.time = time
        msg.mode = ControlMessage.VEHICLE
        if mode == 'pedestrian':
            msg.mode = ControlMessage.PEDESTRIAN

        response = self.send_message(msg)
        return response.result

    def close_door(self):
        msg = ControlMessage()
        msg.id = MSG_ID
        msg.command = ControlMessage.CLOSE

        response = self.send_message(msg)
        return response.result


def main():
    controller = Controller(args.server, 9999)

    if args.command == 'status':
        result = controller.check_status()

    if args.command == 'open':
        result = controller.open_door(args.mode, args.time)

    if args.command == 'close':
        result = controller.close_door()

    print(f'Result: {result} (check spec to know the meaning)')


parser = argparse.ArgumentParser(description='Door Controller')
parser.add_argument('-s', '--server', type=str, default='localhost', help='Server IP Address')

subparsers = parser.add_subparsers(dest='command', help='Commands', metavar='COMMAND')

# Open command with its subarguments
open_parser = subparsers.add_parser('open', help='Open door')
open_parser.add_argument('-t', '--time', type=int, default=0, help='Time to keep the door open in seconds')
open_parser.add_argument('-m', '--mode', choices=['vehicle', 'pedestrian'], default='vehicle', help='Mode to open the door')

close_parser = subparsers.add_parser('close', help='Close door')
get_parser = subparsers.add_parser('status', help='Check door status')

args = parser.parse_args()

if args.command is None:
    parser.print_help()
    exit(1)

main()