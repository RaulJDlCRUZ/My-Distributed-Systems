#!/usr/bin/python3
# Alg. de Cristian con ZeroC Ice (ver. 2)
import time
import ssdd
import Ice
import sys
Ice.loadSlice('cristian.ice')

# Cristian -t -e 1.1:tcp -h 192.168.8.224 -p 4080 -t 60000
# SyncReport -t -e 1.1:tcp -h 192.168.8.224 -p 4080 -t 60000


class Client(Ice.Application):
    def run(self, argv):
        proxy = self.communicator().stringToProxy(argv[1])
        # proxy = self.communicator().stringToProxy('Cristian -t -e 1.1:tcp -h 192.168.8.224 -p 4080 -t 60000')
        _cristian = ssdd.CristianPrx.checkedCast(proxy)

        if not _cristian:
            raise RuntimeError('Invalid proxy')

        # print(_cristian)
        tc1 = time.time()
        print(tc1)
        server_time = _cristian.getServerTime('01234567X', tc1)
        tc2 = time.time()
        print(tc2)
        delta = tc2-tc1
        half_delta = delta/2
        print(delta, half_delta)
        print(server_time)

        new_time = server_time + half_delta

        proxy_2 = self.communicator().stringToProxy(
            'SyncReport -t -e 1.1:tcp -h 192.168.8.224 -p 4080 -t 60000')
        _notify = ssdd.SyncReportPrx.checkedCast(proxy_2)

        if not _notify:
            raise RuntimeError('Invalid proxy 2')

        print(new_time)

        _notify.notifyTime(
            '01234567X', 'Raúl Jiménez de la Cruz', tc2, new_time, half_delta)

        return 0


sys.exit(Client().main(sys.argv))
