#!/usr/bin/env python3

import argparse
import socket
from PaulaCastillejoBravo_Instawhat_pb2 import Release, Response

MSG_ID = 1


class Controller:
    def __init__(self, server_ip, server_port):
        self.server_ip = server_ip
        self.server_port = server_port

    def send_message(self, msg):
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((self.server_ip, self.server_port))

        client.send(msg.SerializeToString())

        response_data = client.recv(1024)
        response = Response()
        response.ParseFromString(response_data)

        client.close()
        return response

    def post(self, url):
        msg = Release()
        msg.id = MSG_ID
        msg.option = Release.POST
        msg.url = url

        response = self.send_message(msg)
        return response.result

    def delete(self, url):
        msg = Release()
        msg.id = MSG_ID
        msg.option = Release.DELETE
        msg.url = url

        response = self.send_message(msg)
        return response.result

    def comments(self, url, remark):
        msg = Release()
        msg.id = MSG_ID
        msg.option = Release.COMMENTS
        msg.url = url
        msg.remark = remark

        response = self.send_message(msg)
        return response.result

    def rate(self, url, assesment):
        msg = Release()
        msg.id = MSG_ID
        msg.option = Release.RATE
        msg.url = url
        msg.points = assesment

        response = self.send_message(msg)
        return response.result

    def like(self, url):
        msg = Release()
        msg.id = MSG_ID
        msg.option = Release.LIKE
        msg.url = url

        response = self.send_message(msg)
        return response.result

    def show(self):
        msg = Release()
        msg.id = MSG_ID
        msg.option = Release.SHOW

        response = self.send_message(msg)
        return response.result


def main():
    controller = Controller(args.server, 2002)

    if args.command == 'post':
        result = controller.post(args.url)

    if args.command == 'delete':
        result = controller.delete(args.url)

    if args.command == 'comment':
        result = controller.comments(args.url, args.remark)

    if args.command == 'rate':
        result = controller.rate(args.url, args.assesment)

    if args.command == 'like':
        result = controller.like(args. url)

    if args.command == 'show':
        result = controller.show()

    print(f'Result: {result} ')


parser = argparse.ArgumentParser(description='Instawhat choice')
parser.add_argument('-s', '--server', type=str,
                    default='localhost', help='Server IP Address')

subparsers = parser.add_subparsers(
    dest='command', help='Commands', metavar='COMMAND')

# Post command
post_parser = subparsers.add_parser('post', help='Post URL photo')
post_parser.add_argument('-u', '--url', type=str, default='', help='URL photo')
# Delete command
delete_parser = subparsers.add_parser('delete', help='Delete URL photo')
delete_parser.add_argument('-u', '--url', type=str,
                           default='', help='URL photo')
# Comments command
comments_parser = subparsers.add_parser('comment', help='Comments photo')
comments_parser.add_argument(
    '-u', '--url', type=str, default='', help='URL photo')
comments_parser.add_argument(
    '-r', '--remark', type=str, default='', help='Remark on the photo')
# Rate command
rate_parser = subparsers.add_parser('rate', help='Rate photo')
rate_parser.add_argument('-u', '--url', type=str, default='', help='URL photo')
rate_parser.add_argument('-a', '--assesment', type=int,
                         default=0, help='Assesment to the photo')
# Like command
like_parser = subparsers.add_parser('like', help='Like photo')
like_parser.add_argument('-u', '--url', type=str, default='', help='URL photo')
# Show command
show_parser = subparsers.add_parser('show', help='Show 20 last photos')


args = parser.parse_args()

if args.command is None:
    parser.print_help()
    exit(1)

main()
