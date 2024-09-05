#!/usr/bin/python3

import socket
import struct
import argparse


def client():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        sending_data = struct.pack('!3sii', 'MUL'.encode(), 34, 54)
        s.sendto(sending_data, ('localhost', 1234))


def server():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.bind(('', 1234))

        msg, _ = s.recvfrom(1024)

        op, num1, num2 = struct.unpack('!3sii', msg)
        op = op.decode()

        if op == 'SUM':
            result = f'{num1} + {num2} = {num1+num2}'
        elif op == 'MUL':
            result = f'{num1} x {num2} = {num1*num2}'
        else:
            result = f'No recognized op'

        print(result)


parser = argparse.ArgumentParser()
parser.add_argument(
    '-m', '--mode',
    type=str,
    choices=['server', 'client'],
    default='server', required=False,
    help='Select the exec mode of the program'
)

args = parser.parse_args()
mode_proc = server if args.mode == 'server' else client
mode_proc()
