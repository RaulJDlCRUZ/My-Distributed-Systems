#!/usr/bin/python3

import sys
import binascii
import argparse
import hashlib
import Ice
import URFS

Ice.loadSlice('urfs.ice')
# CONSTANTES
BLOCK_SIZE = 1024
_DEFAULT_DOWNLOAD_FOLDER = "./downloads/"


class Client(Ice.Application):
    def run(self, argv):
        ic = self.communicator()
        properties = ic.getProperties()

        self.frontend = URFS.FrontendPrx.checkedCast(
            ic.stringToProxy(properties.getProperty('Frontend.Proxy')))

        if not self.frontend:
            raise RuntimeError('Invalid proxy')

        if ARGS.upload:
            self.upload_request(ARGS.upload)

        if ARGS.download:
            self.download_request(ARGS.download)

        if ARGS.remove:
            self.remove_request(ARGS.remove)

        if ARGS.list:
            self.list_request()

    def upload_request(self, file_name):
        try:
            uploader = self.frontend.uploadFile(file_name)
        except URFS.FileNameInUseError:
            print(f'File name ({file_name}) already in use!', flush=True)
            return

        with open(file_name, 'rb') as _file:
            enviados = 0
            while True:
                data = _file.read(BLOCK_SIZE)
                if not data:
                    break
                data = str(binascii.b2a_base64(data, newline=False))
                uploader.send(data)
                enviados += BLOCK_SIZE
                sys.stdout.write('\r' + str(enviados) + ' bytes... ')
                sys.stdout.flush()

        try:
            file_info = uploader.save()
        except URFS.FileAlreadyExistsError as e:
            print(f'File already exists: {e.hash}', flush=True)
            uploader.destroy()
            return

        uploader.destroy()
        print('Upload finished!', flush=True)
        print(f'{file_info.name}: {file_info.hash}', flush=True)

    def download_request(self, dl_hash):
        try:
            downloader = self.frontend.downloadFile(dl_hash)
        except URFS.FileNotFoundError:
            print(f'File with MD5-hash={dl_hash} not found!', flush=True)
            return
        with open(f'{_DEFAULT_DOWNLOAD_FOLDER}{str(dl_hash)}', 'wb') as _file:
            bytes_recibidos = 0
            n_hash = hashlib.md5()
            while True:
                d_data = downloader.recv(BLOCK_SIZE)
                if not d_data:
                    break
                d_data = binascii.a2b_base64(d_data[2:-1])
                _file.write(d_data)
                n_hash.update(d_data)
                bytes_recibidos += len(d_data)
                sys.stdout.write('\r' + str(bytes_recibidos) + ' bytes... ')
                sys.stdout.flush()
            print('Download finished!', flush=True)
        downloader.destroy()

    def remove_request(self, rm_hash):
        try:
            removal = self.frontend.removeFile(rm_hash)
            print(rm_hash, 'removed!')
        except URFS.FileNotFoundError:
            print(f'File with MD5-hash={rm_hash} not found!', flush=True)
            return

    def list_request(self):
        lista = self.frontend.getFileList()

        if not lista:
            print('El servidor no está alojando ningún fichero')
        else:
            print('Lista de Ficheros:\n------------------')
            for x in lista:
                print(f'NAME:{x.name} - HASH:{x.hash}')


if __name__ == '__main__':
    my_parser = argparse.ArgumentParser()
    my_group = my_parser.add_mutually_exclusive_group(required=False)

    my_group.add_argument('-u', '--upload',
                          help='Upload a file to the system, given its path',
                          action='store',
                          type=str,)
    my_group.add_argument('-d', '--download',
                          help='Download a file from the system, given its hash',
                          action='store',
                          type=str,)
    my_group.add_argument('-r', '--remove',
                          help='Remove a file from the system, given its hash',
                          action='store',
                          type=str,)
    my_group.add_argument('-l', '--list',
                          help='List all files in the system',
                          action='store_true',
                          default=False)

    ARGS, unknown = my_parser.parse_known_args()
    sys.exit(Client().main(sys.argv))
