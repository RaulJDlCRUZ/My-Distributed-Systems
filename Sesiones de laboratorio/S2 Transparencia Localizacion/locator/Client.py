#!/usr/bin/python3

import sys
import Example
import Ice
Ice.loadSlice('Printer.ice')


class Client(Ice.Application):
    def run(self, argv):
        # proxy = self.communicator().stringToProxy(argv[1])
        ic = self.communicator()
        properties = ic.getProperties()
        
        # proxys = self.communicator().stringToProxy("Server.Proxy")
        proxys = properties.getProperty("Server.Proxy")
        print("\t:",proxys,"\n\n")
        printer = Example.PrinterPrx.checkedCast(ic.stringToProxy(proxys))

        if not printer:
            raise RuntimeError('Invalid proxy')

        printer.write('Hello World!')

        return 0


sys.exit(Client().main(sys.argv))