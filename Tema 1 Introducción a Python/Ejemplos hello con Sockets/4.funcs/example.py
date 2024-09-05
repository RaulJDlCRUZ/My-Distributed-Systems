#!/usr/bin/python3

import socket
import argparse


def client():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.sendto("hello".encode(), ('localhost', 1234))


def server():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.bind(('', 1234))
        msg, client = s.recvfrom(1024)
        print(msg.decode(), client)



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
