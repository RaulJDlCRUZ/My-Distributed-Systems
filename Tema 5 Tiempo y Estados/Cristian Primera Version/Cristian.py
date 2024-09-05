#!/usr/bin/python3
# Alg. de Cristian con ZeroC Ice (ver. 1)

import Cristian
import sys
import datetime
import Ice
Ice.loadSlice('Cristian.ice')


class Client(Ice.Application):
    def run(self, argv):
        proxy = self.communicator().stringToProxy(argv[1])
        timeprinter = Cristian.TimePrinterPrx.checkedCast(proxy)

        if not timeprinter:
            raise RuntimeError('Invalid proxy')

        time_client_1 = 1000*datetime.datetime.now().timestamp()
        time_server = float(timeprinter.write())
        time_client_2 = 1000*datetime.datetime.now().timestamp()
        delta_client = time_client_2-time_client_1
        cristian = time_server + 0.5*(delta_client)

        print(f'T1={datetime.datetime.fromtimestamp(time_client_1/1000.0)}\
                \n\t\tTS={datetime.datetime.fromtimestamp(time_server/1000.0)}\
                \nT2={datetime.datetime.fromtimestamp(time_client_2/1000.0)}\
                \n\nDelta={delta_client}\
                \nCristian={datetime.datetime.fromtimestamp(cristian/1000.0)}\
                \nError=+-{delta_client/2}')
        return 0


sys.exit(Client().main(sys.argv))
