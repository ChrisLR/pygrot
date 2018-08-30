import pytest

from pygrot.client import game
from pygrot.client.networking import udpclient
from pygrot.server.networking import udpserver
from pygrot.netmessages import listing


def test_sends_join_request_on_initialize(game_client):
    game_client.connect()
    client_messages = game_client.echo_protocol.intercepted_messages
    server, sub_messages = client_messages[0]
    sub_message = sub_messages[0]

    assert isinstance(sub_message, listing.JoinRequest)


def test_sends_disconnect_request(game_client):
    game_client.server = udpclient.AbstractServer(("test", "test"))
    game_client.disconnect()
    client_messages = game_client.echo_protocol.intercepted_messages
    server, sub_messages = client_messages[0]
    sub_message = sub_messages[0]

    assert isinstance(sub_message, listing.DisconnectRequest)


def test_sends_key_input(game_client):
    game_client.server = udpclient.AbstractServer(("test", "test"))
    game_client.entity_uid = "test"
    game_client.send_input("F", "T")
    client_messages = game_client.echo_protocol.intercepted_messages
    server, sub_messages = client_messages[0]
    sub_message = sub_messages[0]

    assert isinstance(sub_message, listing.KeyInput)
    assert sub_message.entity_uid == "test"
    assert sub_message.symbol == "F"
    assert sub_message.modifiers == "T"


def test_handles_complete_update(game_client):
    entity = udpserver.AbstractEntity("e1", "skeleton", (0, 0))
    game_client.game = game.Game(game_client)
    game_client.game.initialize_game()
    game_client.game.spawn_entity(entity.uid, entity.name, entity.position)
    game_client.receive_update({
        "e1": udpserver.AbstractEntity("e1", "skeleton", (1, 0)),
        "e2": udpserver.AbstractEntity("e2", "skeleton", (2, 0)),
    })

    assert len(game_client.game.entities) == 2
    assert game_client.game.entities["e1"].move_to == (1, 0)
    assert game_client.game.entities["e2"].location.tuple() == (2, 0)


class FakeProtocol(object):
    def __init__(self):
        self.intercepted_messages = []

    def send(self, client, messages, sender):
        self.intercepted_messages.append((client, messages))


@pytest.fixture
def game_client():
    return udpclient.GameClient(FakeProtocol())
