import json
import uuid

from twisted.internet import reactor
from twisted.internet.protocol import DatagramProtocol

from pygrot.gamedata import monsters
from pygrot.netmessages import listing


class Echo(DatagramProtocol):
    def datagramReceived(self, data, info):
        host, port = info
        self.transport.write("got that".encode("utf8"), (host, 9000))


def build_message(data):
    decoded_data = data.decode("utf8")
    message_capsule = json.loads(decoded_data)
    messages = message_capsule.get("netmessages")
    if messages is None:
        print("Unrecognized message " + decoded_data)
        return

    built_messages = []
    for message in messages:
        type_no = message.get("type_no")
        sub_message = message.get("message")
        if type_no is None or sub_message is None:
            print("Unrecognized sub message " + message)
            continue

        mapped_type = listing.message_mapping.get(type_no)
        instanced_type = mapped_type(**sub_message)
        built_messages.append(instanced_type)

    return built_messages


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
        address = message.sender
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


class RemoteClient(object):
    """Client as Seen from the Server"""

    def __init__(self, address, entity_uid):
        self.address = address
        self.entity_uid = entity_uid


class RemoteEntity(object):
    def __init__(self, entity_uid, entity_name):
        self.entity_uid = entity_uid
        self.entity_name = entity_name


def create_new_entity():
    return RemoteEntity(uuid.uuid4(), monsters.Skeleton.name)


if __name__ == '__main__':
    server = Server()
    reactor.listenUDP(9001, server.echo_protocol)
    reactor.run()
