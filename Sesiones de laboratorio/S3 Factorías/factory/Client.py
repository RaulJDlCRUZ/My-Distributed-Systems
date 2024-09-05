#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-

import sys
import Ice
Ice.loadSlice('-I. --all PrinterFactory.ice')
import Example


class Client(Ice.Application):
    def run(self, argv):
        proxy = self.communicator().stringToProxy(argv[1])
        factory = Example.PrinterFactoryPrx.checkedCast(proxy)

        if not factory:
            raise RuntimeError('Invalid proxy')

        printer = factory.create("Printer1")
        printer.write('Hello World!')
        printer.destroy()

        return 0


sys.exit(Client().main(sys.argv))
