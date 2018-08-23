from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor
from serializing.netserializer import NetworkSerializer, NetworkComm
import json


class Echo(DatagramProtocol):
    def datagramReceived(self, data, info):
        host, port = info
        json_data = json.loads(data)
        print("received %r from %s:%d" % (NetworkComm(**json_data), host, port))


if __name__ == '__main__':
    reactor.listenUDP(9000, Echo())
    reactor.run()
