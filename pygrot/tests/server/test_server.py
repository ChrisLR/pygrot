from pygrot.netmessages import listing
from pygrot.server.networking.udpserver import Server


def test_accepts_new_client():
    fake_protocol = FakeProtocol()
    server = Server(fake_protocol)
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


def test_handles_key_input():
    raise NotImplementedError()


def test_handles_disconnect():
    raise NotImplementedError()


def test_sends_messages():
    raise NotImplementedError()


class FakeProtocol(object):
    def __init__(self):
        self.intercepted_messages = []

    def send(self, client, messages):
        self.intercepted_messages.append((client, messages))
