#!/usr/bin/python3

import sys
import Ice
Ice.loadSlice('Math.ice')
import Calculator

class Client(Ice.Application):
    def run(self, argv):
        proxy = self.communicator().stringToProxy(argv[1])
        mymath = Calculator.MathPrx.uncheckedCast(proxy)
        
        if not mymath:
            raise RuntimeError('Invalid proxy')

        try:
            first_operator = int(sys.argv[2])
            second_operator = int(sys.argv[4])
            
            if sys.argv[3] == 'TIMES':
                mymath.mult(first_operator, second_operator)
            else:
                print("THE RESULT OF THE SUM IS {0}".format(mymath.sum(first_operator, second_operator)))
        except Exception as e:
            print(e)
            exit(-1)

        return 0
    
def error():
    print('Usage: {0} $(shell head -1 proxy.out) <OP1> <PLUS/TIMES> <O2>', sys.argv[0])
    exit(-1)

if __name__ == '__main__':
    if len(sys.argv)!=5:
        error()
    
    if sys.argv[3] not in ('PLUS', 'TIMES'):
        error()
    
    sys.exit(Client().main(sys.argv))