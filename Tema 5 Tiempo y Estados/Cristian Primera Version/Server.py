#!/usr/bin/python3 -u
import Cristian
import datetime
import sys
import Ice

Ice.loadSlice('Cristian.ice')


class TimePrinterI(Cristian.TimePrinter):
    # n = 0
    def write(self, current=None):
        return str(1000*datetime.datetime.now().timestamp())


class Server(Ice.Application):
    def run(self, argv):
        broker = self.communicator()
        servant = TimePrinterI()

        adapter = broker.createObjectAdapter("TimePrinterAdapter")
        proxy = adapter.add(servant, broker.stringToIdentity("timeprinter1"))

        print(proxy, flush=True)

        adapter.activate()
        self.shutdownOnInterrupt()
        broker.waitForShutdown()

        return 0


server = Server()
try:
    sys.exit(server.main(sys.argv))
except KeyboardInterrupt:
    pass
