import time
import uuid

import pyglet

from pygrot.gamedata import monsters
from pygrot.netmessages import listing
from pygrot.netmessages.echoprotocol import Echo


class Server(object):
    CLIENT_PORT = 9000
    SERVER_PORT = 9001

    def __init__(self, echo_protocol=None):
        self.entities = {}
        self.message_handlers = {
            listing.KeyInput: self.handle_input,
            listing.DisconnectRequest: self.disconnect_client,
        }
        self.echo_protocol = Echo(self.SERVER_PORT, 'localhost', self.CLIENT_PORT) if echo_protocol is None else echo_protocol
        self.registered_clients = {}
        self.started = False

    def handle_messages(self, sender, messages):
        client = self.registered_clients.get(sender)
        if client is None:
            join_request = next(message for message in messages if isinstance(message, listing.JoinRequest))
            if join_request is None:
                return
            else:
                return self.accept_new_client(sender, join_request)

        for message in messages:
            if isinstance(message, listing.JoinRequest):
                del self.registered_clients[sender]
                return self.accept_new_client(sender, message)

            handler = self.message_handlers.get(type(message))
            handler(client, message)

    def accept_new_client(self, sender, message):
        new_entity = create_new_entity()
        new_client = RemoteClient(sender, new_entity)
        self.registered_clients[sender] = new_client
        accept_message = listing.JoinAccept(new_entity)
        update_message = listing.CompleteUpdate(self.entities)
        self.entities[new_entity.uid] = new_entity
        self.send(new_client, (accept_message, update_message))

    def disconnect_client(self, client, message):
        del self.registered_clients[client.address]
        del self.entities[client.remote_entity.uid]

    def update(self):
        remote_info, messages = self.echo_protocol.get()
        if remote_info is not None and messages is not None:
            self.handle_messages(remote_info, messages)

        self.complete_update()

    def complete_update(self):
        update_message = listing.CompleteUpdate(self.entities)
        for address, client in self.registered_clients.items():
            self.send(client, (update_message,))

    def handle_input(self, client, message):
        entity_uid = message.entity_uid
        entity = self.entities.get(entity_uid)
        symbol = message.symbol
        if entity is None:
            print("WTF UNKNOWN ENTITY UID " + entity_uid)

        px, py = entity.position
        if symbol == pyglet.window.key.LEFT:
            px -= 16
        if symbol == pyglet.window.key.UP:
            py += 16
        if symbol == pyglet.window.key.RIGHT:
            px += 16
        if symbol == pyglet.window.key.DOWN:
            py -= 16

        entity.position = (px, py)

    def send(self, client, messages):
        self.echo_protocol.send(client, messages, "SERVER")

    def start(self):
        print("Server starting echo protocol")
        self.echo_protocol.start()
        self.started = True
        while self.started:
            self.update()
            time.sleep(0.01)


class RemoteClient(object):
    """Client as Seen from the Server"""

    def __init__(self, address, remote_entity):
        self.address = address
        self.remote_entity = remote_entity


class AbstractEntity(object):
    def __init__(self, uid, name, position):
        self.uid = uid
        self.name = name
        self.position = position


def create_new_entity():
    return AbstractEntity(uuid.uuid4().urn, monsters.Skeleton.name, (0, 0))


if __name__ == '__main__':
    server = Server()
    server.start()
