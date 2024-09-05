#!/usr/bin/python3

import sys
import Ice
Ice.loadSlice('Printer.ice')
import Example


class PrinterI(Example.Printer):
    def __init__(self, name):
        self.name = name

    def write(self, message, current=None):
        print("{0}: {1}".format(self.name, message))
        sys.stdout.flush()


class Server(Ice.Application):
    def run(self, argv):
        ic = self.communicator()
        properties = ic.getProperties()
        servant = PrinterI(properties.getProperty("Ice.ProgramName"))

        adapter = ic.createObjectAdapter("PrinterAdapter")
        servant_id = properties.getProperty("identity")
        proxy = adapter.add(servant, ic.stringToIdentity(servant_id))

        print(proxy, flush=True)

        adapter.activate()
        self.shutdownOnInterrupt()
        ic.waitForShutdown()

        return 0


server = Server()
sys.exit(server.main(sys.argv))
