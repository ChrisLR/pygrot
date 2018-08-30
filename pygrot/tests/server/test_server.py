import pyglet
import pytest

from pygrot.netmessages import listing
from pygrot.server.networking import udpserver


def test_accepts_new_client(server):
    fake_protocol = server.echo_protocol
    server.accept_new_client("127.0.0.1", None)
    server_message = fake_protocol.intercepted_messages

    client, sub_messages = server_message[0]
    accept, update = sub_messages
    new_uid = accept.entity.uid

    assert new_uid
    assert isinstance(accept, listing.JoinAccept)
    assert isinstance(update, listing.CompleteUpdate)
    assert len(update.entities) == 1
    assert update.entities[new_uid]


def test_handles_key_input(server, fake_entity):
    server.entities["test_1"] = fake_entity
    fake_message = listing.KeyInput(pyglet.window.key.LEFT, None, "test_1")
    server.handle_input(None, fake_message)

    assert server.entities["test_1"].position == (-16, 0)


def test_handles_disconnect(server, fake_client):
    server.registered_clients[fake_client.address] = fake_client
    server.entities[fake_client.remote_entity.uid] = fake_client.remote_entity
    server.disconnect_client(fake_client, None)

    assert fake_client.address not in server.registered_clients
    assert fake_client.remote_entity.uid not in server.entities


def test_sends_complete_updates(server, fake_client, fake_entity):
    server.registered_clients[fake_client.address] = fake_client
    server.entities[fake_client.remote_entity.uid] = fake_client.remote_entity
    server.complete_update()
    server_message = server.echo_protocol.intercepted_messages
    client, sub_messages = server_message[0]
    sub_message = sub_messages[0]

    assert len(sub_messages) == 1
    assert isinstance(sub_message, listing.CompleteUpdate)
    assert fake_entity.uid in sub_message.entities
    assert sub_message.entities[fake_entity.uid] == fake_entity


def test_handles_messages(server):
    join_request = listing.JoinRequest("")

    disconnect_request = listing.DisconnectRequest("")
    server.handle_messages(("127.0.0.1", "9000"), (join_request,))
    assert len(server.registered_clients) == 1

    entity = list(server.entities.values())[0]
    key_input_request = listing.KeyInput("", "", entity.uid)
    server.handle_messages(("127.0.0.1", "9000"), (key_input_request,))
    assert len(server.entities) == 1

    server.handle_messages(("127.0.0.1", "9000"), (disconnect_request,))
    assert len(server.registered_clients) == 0
    assert len(server.entities) == 0


class FakeProtocol(object):
    def __init__(self):
        self.intercepted_messages = []

    def send(self, client, messages, sender):
        self.intercepted_messages.append((client, messages))


@pytest.fixture
def server():
    return udpserver.Server(FakeProtocol())


@pytest.fixture
def fake_client(fake_entity):
    return udpserver.RemoteClient(("127.0.0.1", "9000"), fake_entity)


@pytest.fixture
def fake_entity():
    return udpserver.AbstractEntity("test_1", "Skeleton", (0, 0))
