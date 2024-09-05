#!/usr/bin/python3 -u

import sys
import Ice
import Calculator
import Example
Ice.loadSlice('Math.ice')
Ice.loadSlice('Printer.ice')

proxyprinter=""

class CalculatorI(Calculator.Math):
    def mult(self, x, y, context=None):
        # Este print ahora debe ser un printer
        print("THE RESULT OF THE PRODUCT IS {0}".format(str(x * y)))
        printer = Example.PrinterPrx.checkedCast(proxyprinter)

        if not printer:
            raise RuntimeError('Invalid proxy')

        printer.write("{0}".format(str(x*y)))
        return x * y
        
    def sum(self, x, y, context=None):
        return x + y

class Server(Ice.Application):
    def run(self, argv):    
        global proxyprinter
        broker = self.communicator()
        
        mathadapter = broker.createObjectAdapter("MathAdapter")
        mathservant = CalculatorI()
        mathproxy = mathadapter.add(mathservant, broker.stringToIdentity("math1"))
        print(mathproxy, flush=True)
        
        proxyprinter = self.communicator().stringToProxy(argv[1])
        mathadapter.activate()
            
        self.shutdownOnInterrupt()
        broker.waitForShutdown()
        return 0

server = Server()
sys.exit(server.main(sys.argv))