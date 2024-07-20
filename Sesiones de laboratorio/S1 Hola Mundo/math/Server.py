#!/usr/bin/python3 -u

import sys
import Ice

Ice.loadSlice('Math.ice')
import Calculator

class CalculatorI(Calculator.Math):
    def mult(self, x, y, context=None):
        print("THE RESULT OF THE PRODUCT IS {0}".format(str(x * y)))
    def sum(self, x, y, context=None):
        return x + y

class Server(Ice.Application):
    def run(self, argv):
        broker = self.communicator()
        mathservant = CalculatorI()
        mathadapter = broker.createObjectAdapter("MathAdapter")
        mathproxy = mathadapter.add(mathservant, broker.stringToIdentity("math1"))
        print(mathproxy, flush=True)
        mathadapter.activate()
        self.shutdownOnInterrupt()
        broker.waitForShutdown()
        return 0

server = Server()
sys.exit(server.main(sys.argv))