#!/usr/bin/python3

import sys
import Ice
import URFS
import IceStorm

Ice.loadSlice('urfs.ice')
# CONSTANTES
TOPICS = ["FileUpdatesTopic", "FrontendUpdatesTopic"]
ADAPTERS = ["FrontendAdapter", "FileUpdatesAdapter", "FrontendUpdatesAdapter"]
# Secuencia de estructuras FileInfo
FileList = []


class FileNameInUseError(URFS.FileNameInUseError):
    '''Excepción que comprueba si el nombre del fichero ya figura en el registro'''

    def __init__(self):
        pass


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


class FileUpdatesI(URFS.FileUpdates):
    '''Clase con métodos necesarios para el canal de eventos FileUpdates'''

    def new(self, file, current):
        '''Agrega un archivo al registro'''
        print(file.fileInfo.name, file.fileInfo.hash, file.fileManager)
        if file.fileInfo not in FileList:  # !evitamos archivos duplicados
            FileList.append(file.fileInfo)
        print(FileList)

    def removed(self, file, current):
        '''Elimina un archivo del registro'''
        print(file.fileInfo.hash, file.fileManager)
        FileList.remove(FrontendI(file.fileManager).getFileInfo(
            file.fileInfo.hash, current))
        print(FileList)


class FrontendUpdatesI(URFS.FrontendUpdates):
    '''Clase con métodos necesarios para el canal de eventos FileUpdates'''

    def __init__(self, broker, filemanager):
        self.broker = broker
        self.filemanager = filemanager

    def get_topic_manager(self):
        key = 'IceStorm.TopicManager.Proxy'
        proxy = self.broker.propertyToProxy(key)
        if proxy is None:
            print("property '{}' not set".format(key))
            return None

        print("Using IceStorm in: '%s'" % key)
        return IceStorm.TopicManagerPrx.checkedCast(proxy)

    def newFrontend(self, newFrontend, current):
        '''Método que recibe por el canal de eventos FrontendUpdates un nuevo Frontend'''
        print('[FU] Sync and sending files...', newFrontend)
        newFrontend.replyNewFrontend(newFrontend)
        topic_mgr = self.get_topic_manager()
        if not topic_mgr:
            print("Invalid Proxy Topic Manager")
            return 1
        try:
            topic = topic_mgr.create(TOPICS[0])
        except IceStorm.TopicExists:
            topic = topic_mgr.retrieve(TOPICS[0])

        f_u_publisher = topic.getPublisher()
        file_updates = URFS.FileUpdatesPrx.uncheckedCast(f_u_publisher)

        if not file_updates:
            print("Invalid Proxy File Updates")
            return 2

        for i in FileList:
            file_updates.new(FileData(i, self.filemanager))


class FrontendI(URFS.Frontend):
    '''Objeto Frontend'''

    def __init__(self, filemanager):
        self.filemanager = filemanager

    def getFileList(self, current):
        '''Listado con todos los ficheros que figuran en el registro del Frontend. Elementos FileInfo'''
        print('[FE] list')
        return FileList.copy()

    def getFileInfo(self, file_hash, current):
        '''Obtener estructura FileInfo en base a un hash'''
        file_to_get = None
        for x in FileList.copy():
            if x.hash == file_hash:
                file_to_get = FileInfo(x.name, file_hash)
        return file_to_get

    def replyNewFrontend(self, oldFrontEnd, current):
        '''Respuesta con el proxy directo del Frontend por el canal de eventos FrontendUpdates'''
        print("[rFU]", oldFrontEnd)

    def uploadFile(self, filename, current):
        '''Este método devolverá referencia a un objeto Uploader para subir un fichero. Excepción si ya existe'''
        print(f'[FE] upload {filename}')
        if any(x for x in FileList if x.name == filename):
            print(f'{filename} ya está en el servidor')
            raise FileNameInUseError()
        return self.filemanager.createUploader(filename)

    def downloadFile(self, hash, current):
        '''Este método devolverá referencia a un objeto Downloader para descargar un fichero. Excepción no ya existe'''
        print(f'[FE] download {hash}')
        file = self.getFileInfo(hash, current)
        if file is None:
            print(f'{hash} no está en el servidor')
            raise FileNotFoundError()
        return self.filemanager.createDownloader(hash)

    def removeFile(self, hash, current):
        '''Este método devolverá referencia de FileManager para eliminar un fichero. Excepción si no existe'''
        print(f'[FE] remove {hash}')
        file = self.getFileInfo(hash, current)
        if file is None:
            print(f'{hash} no está en el servidor')
            raise FileNotFoundError()
        return self.filemanager.removeFile(hash)


class Server(Ice.Application):
    '''Servidor para Frontend'''

    def get_topic_manager(self):
        key = 'IceStorm.TopicManager.Proxy'
        proxy = self.communicator().propertyToProxy(key)
        if proxy is None:
            print("property '{}' not set".format(key))
            return None

        print("Using IceStorm in: '%s'" % key)
        return IceStorm.TopicManagerPrx.checkedCast(proxy)

    def run(self, argv):
        broker_ic = self.communicator()
        properties = broker_ic.getProperties()

        self.filemanager = URFS.FileManagerPrx.checkedCast(
            broker_ic.stringToProxy(properties.getProperty('FileManager.Proxy')))

        if not self.filemanager:
            raise RuntimeError('Invalid Proxy File Manager')

        topic_mgr = self.get_topic_manager()

        servant = FrontendI(self.filemanager)
        adapter = broker_ic.createObjectAdapter(ADAPTERS[0])
        proxy = adapter.add(servant, broker_ic.stringToIdentity("frontend1"))
        print(proxy, flush=True)
        adapter.activate()

        # ----SUSCRIPTOR FILE UPDATES-----
        file_updates_servant = FileUpdatesI()
        file_updates_adapter = broker_ic.createObjectAdapter(ADAPTERS[1])
        file_updates_subscriber = file_updates_adapter.addWithUUID(
            file_updates_servant)
        file_updates_proxy = file_updates_adapter.createDirectProxy(
            file_updates_subscriber.ice_getIdentity())

        if not topic_mgr:
            print("Invalid Proxy Topic Manager")
            return 1

        try:
            topic_0 = topic_mgr.create(TOPICS[0])
        except IceStorm.TopicExists:
            topic_0 = topic_mgr.retrieve(TOPICS[0])
        topic_0.subscribeAndGetPublisher({}, file_updates_proxy)

        file_updates_adapter.activate()

        # ----FRONTEND UPDATES----
        frontend_updates_servant = FrontendUpdatesI(
            broker=broker_ic, filemanager=self.filemanager)
        frontend_updates_adapter = broker_ic.createObjectAdapter(ADAPTERS[2])

        try:
            topic_1 = topic_mgr.create(TOPICS[1])
        except IceStorm.TopicExists:
            topic_1 = topic_mgr.retrieve(TOPICS[1])

        frontend_updates_adapter.activate()
        frontend_updates_publisher = topic_1.getPublisher()
        frontendupdates = URFS.FrontendUpdatesPrx.uncheckedCast(
            frontend_updates_publisher)

        if not frontendupdates:
            print("Invalid Proxy, ", ADAPTERS[2])
            return 2

        # para evitar una respuesta del evento lanzado del mismo frontend (para obtener la de los demás), publico primero y luego suscribo...
        frontendupdates.newFrontend(URFS.FrontendPrx.checkedCast(
            adapter.createDirectProxy(proxy.ice_getIdentity())))

        frontend_updates_subscriber = frontend_updates_adapter.addWithUUID(
            frontend_updates_servant)
        frontend_updates_proxy = frontend_updates_adapter.createDirectProxy(
            frontend_updates_subscriber.ice_getIdentity())
        topic_1.subscribeAndGetPublisher({}, frontend_updates_proxy)

        print(
            f'ZeroC Ice version: {Ice.stringVersion()}\nFrontend Proxy: {proxy}', flush=True)
        print(
            f'Waiting events for FileUpdates Channel...{file_updates_proxy}\nWaiting events for FrontendUpdates Channel...{frontend_updates_proxy}')

        # ---- ESPERAR A CONTROL+C ----
        self.shutdownOnInterrupt()
        broker_ic.waitForShutdown()
        topic_0.unsubscribe(file_updates_subscriber)
        topic_1.unsubscribe(frontend_updates_subscriber)
        return 0


server = Server()
sys.exit(server.main(sys.argv))
