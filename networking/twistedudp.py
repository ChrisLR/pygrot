from twisted.internet.protocol import DatagramProtocol


class Listen(DatagramProtocol):
    def __init__(self, listener):
        super().__init__()
        self.listener = listener

    def datagramReceived(self, data, info):
        host, port = info
        self.listener.handle_message(data, host, port)
