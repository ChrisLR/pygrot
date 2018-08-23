from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor
import json


class Echo(DatagramProtocol):
    def datagramReceived(self, data, info):
        host, port = info
        print()


if __name__ == '__main__':
    reactor.listenUDP(9000, Echo())
    reactor.run()
