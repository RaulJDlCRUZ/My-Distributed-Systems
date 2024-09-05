#!/usr/bin/python3
import sys
import os
import binascii
import hashlib
import Ice
import URFS
import IceStorm
# CONSTANTES
BLOCK_SIZE = 1024
_DEFAULT_UPLOADED_FOLDER = "./storage/"

Ice.loadSlice('urfs.ice')


class FileAlreadyExistsError(URFS.FileAlreadyExistsError):
    '''Excepción que comprueba si ya existe un fichero con ese hash'''

    def __init__(self, hash):
        self.hash = hash


class FileNotFoundError(URFS.FileNotFoundError):
    '''Excepción que comprueba si el nombre del fichero no figura en el registro'''

    def __init__(self):
        pass


class FileInfo(URFS.FileInfo):
    '''Estructura que contienen el nombre del fichero y su hash'''

    def __init__(self, name, hash):
        self.name = name
        self.hash = hash


class FileData(URFS.FileData):
    '''Estructura con la información del archivo y la referencia del FileManager que lo gestiona'''

    def __init__(self, fileInfo, fileManager):
        self.fileInfo = fileInfo
        self.fileManager = fileManager


class FileManagerI(URFS.FileManager):
    '''Objeto FileManager'''

    def __init__(self):
        self.fm_ref = None
        self.file_updates = None

    # Clases Internas para File Manager
    class DownloaderI(URFS.Downloader):
        '''Objeto Downloader'''

        def __init__(self, f):
            self.df = f

        def recv(self, size, current):
            '''Procedimiento que obtiene datos del archivo y los devuelve como cadena'''
            while True:
                data = self.df.read(size)
                if not data:
                    break
                return str(binascii.b2a_base64(data, newline=False))

        def destroy(self, current):
            '''Destrucción explícita del objeto Downloader'''
            current.adapter.remove(current.id)
            print(f'{self.df} downloader destroyed', flush=True)

    class UploaderI(URFS.Uploader):
        '''Objeto Uploader'''

        def __init__(self, f, file_updates, file_manager_proxy):
            self.uf = f
            self.hash = hashlib.md5()
            self.file_updates = file_updates
            self.file_m_proxy = file_manager_proxy

        def send(self, data, current):
            '''Procedimiento que recibe datos y los almacena en un fichero, además de actualizar su hash'''
            new_data = binascii.a2b_base64(data[2:-1])
            self.uf.write(new_data)
            self.hash.update(new_data)

        def save(self, current):
            '''Procedimiento que cambiará el nombre del fichero subido para almacenarlo en el servidor. Fallará si ya existe el hash en la carpeta del servidor'''
            self.uf.close()
            original_name = self.uf.name
            final_hash = f'{str(self.hash.hexdigest())}'

            if os.path.exists(f'{_DEFAULT_UPLOADED_FOLDER}{final_hash}'):
                print(
                    f'[U] {final_hash} ya se encuentra alojado en el servidor')
                os.remove(f'{self.uf.name}')
                raise FileAlreadyExistsError(final_hash)
            else:
                os.rename(original_name,
                          f'{_DEFAULT_UPLOADED_FOLDER}{final_hash}')
                new_file = FileInfo(
                    f'{original_name.split("/")[-1]}', f'{str(self.hash.hexdigest())}')
                file = FileData(new_file, self.file_m_proxy)
                self.file_updates.new(file)
                return new_file

        def destroy(self, current):
            '''Destrucción explícita del objeto Uploader'''
            current.adapter.remove(current.id)
            print(f'{self.uf} uploader destroyed', flush=True)

    # Métodos para FileManager
    def hashSearch(self, srch_hash):
        '''Método de apoyo para comprobar si en la carpeta del servidor existe un fichero'''
        retval = 0
        for root, dirs, files in os.walk(_DEFAULT_UPLOADED_FOLDER, topdown=False):
            for name in files:
                if str(name) == str(srch_hash):
                    retval = 1
        return retval

    def createUploader(self, filename, current):
        '''Crea un objeto Uploader y devuelve su referencia (proxy)'''
        f = open(f'{_DEFAULT_UPLOADED_FOLDER}{filename}', 'wb')
        return URFS.UploaderPrx.checkedCast(current.adapter.addWithUUID(self.UploaderI(f, self.file_updates, self.fm_ref)))

    def createDownloader(self, hash, current):
        '''Crea un objeto Downloader y devuelve su referencia (proxy). Fallará si no existe el fichero a descargar'''
        if self.hashSearch(hash) != 1:
            print(f'[D] {hash} no se encuentra en el servidor')
            raise FileNotFoundError()

        f = open(f'{_DEFAULT_UPLOADED_FOLDER}{hash}', 'rb')
        return URFS.DownloaderPrx.checkedCast(current.adapter.addWithUUID(self.DownloaderI(f)))

    def removeFile(self, hash, current):
        '''Procedimiento que eliminará un fichero de la carpeta del servidor. Fallará si este fichero no existe'''
        if self.hashSearch(hash) != 1:
            print(f'[R] {hash} no se encuentra en el servidor')
            raise FileNotFoundError()
        else:
            os.remove(os.path.join(_DEFAULT_UPLOADED_FOLDER, str(hash)))
            file = FileData(FileInfo(name='', hash=str(hash)), self.fm_ref)
            self.file_updates.removed(file)


class Server(Ice.Application):
    '''Servidor para FileManager'''

    def get_topic_manager(self):
        key = 'IceStorm.TopicManager.Proxy'
        proxy = self.communicator().propertyToProxy(key)
        if proxy is None:
            print("property {} not set".format(key))
            return None

        print("Using IceStorm in: '%s'" % key)
        return IceStorm.TopicManagerPrx.checkedCast(proxy)

    def run(self, argv):
        ic = self.communicator()
        properties = ic.getProperties()
        servant = FileManagerI()
        adapter = ic.createObjectAdapter("FileManagerAdapter")

        proxy = adapter.add(servant, ic.stringToIdentity("filemanager1"))
        print(proxy, flush=True)
        #   - - CANAL DE EVENTOS: PUBLICADOR 1 - -
        topic_name = "FileUpdatesTopic"

        topic_mgr = self.get_topic_manager()
        if not topic_mgr:
            print("Invalid Proxy Topic Manager")
            return 1
        try:
            topic = topic_mgr.create(topic_name)
        except IceStorm.TopicExists:
            topic = topic_mgr.retrieve(topic_name)

        f_u_publisher = topic.getPublisher()
        servant.file_updates = URFS.FileUpdatesPrx.uncheckedCast(f_u_publisher)

        if not servant.file_updates:
            print("Invalid Proxy File Updates")
            return 2

        servant.fm_ref = URFS.FileManagerPrx.checkedCast(proxy)

        adapter.activate()
        self.shutdownOnInterrupt()
        ic.waitForShutdown()

        return 0


server = Server()
sys.exit(server.main(sys.argv))
