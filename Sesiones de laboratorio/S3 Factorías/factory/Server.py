#!/usr/bin/python3

import sys
import Ice
Ice.loadSlice('PrinterFactory.ice')
import Example


class PrinterI(Example.Printer):
    def __init__(self, name):
        self.name = name

    def write(self, message, current):
        print(f'{self.name} says: {message}', flush=True)

    def destroy(self, current):
        current.adapter.remove(current.id)
        print(f'{self.name} destroyed', flush=True)


class PrinterFactoryI(Example.PrinterFactory):
    def create(self, name, current):
        servant = PrinterI(name)
        proxy = current.adapter.addWithUUID(servant)
        return Example.PrinterPrx.checkedCast(proxy)


class Server(Ice.Application):
    def run(self, argv):
        ic = self.communicator()
        servant = PrinterFactoryI()

        adapter = ic.createObjectAdapter("PrinterFactoryAdapter")
        proxy = adapter.add(servant, ic.stringToIdentity("PF1"))

        print(proxy, flush=True)

        adapter.activate()
        self.shutdownOnInterrupt()
        ic.waitForShutdown()

        return 0


server = Server()
sys.exit(server.main(sys.argv))

