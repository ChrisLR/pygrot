from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor
import json
from networking.messages import listing


class Echo(DatagramProtocol):
    def datagramReceived(self, data, info):
        host, port = info
        self.transport.write("got that".encode("utf8"), (host, 9000))


class Server(object):
    def __init__(self):
        self.message_handlers = {
            listing.JoinRequest: self.accept_new_client,
            listing.KeyInput: self.handle_input,
            listing.DisconnectRequest: self.disconnect_client,
        }
        self.echo_protocol = Echo()
        self.registered_clients = []

    def accept_new_client(self, message):
        # Add RemoteClient to registered Clients
        # Call assign New Entity
        # Send AcceptMessage
        pass

    def disconnect_client(self, message):
        pass

    def complete_update(self):
        # Create new Message Capsule
        # Send List of Tuples with Position, entity_id
        pass

    def handle_input(self, message):
        pass


if __name__ == '__main__':
    server = Server()
    reactor.listenUDP(9001, server.echo_protocol)
    reactor.run()
