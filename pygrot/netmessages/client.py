import abc

from pygrot.netmessages.base import BaseMessage


class ClientMessage(BaseMessage, metaclass=abc.ABCMeta):
    pass


class DisconnectRequest(ClientMessage):
    type_no = 1

    def __init__(self, username):
        super().__init__()
        self.username = username

    def to_json(self):
        return {"username": self.username}


class JoinRequest(ClientMessage):
    type_no = 2

    def __init__(self, username):
        super().__init__()
        self.username = username

    def to_json(self):
        return {"username": self.username}


class KeyInput(ClientMessage):
    type_no = 3

    def __init__(self, symbol, modifiers, entity_uid):
        super().__init__()
        self.symbol = symbol
        self.modifiers = modifiers
        self.entity_uid = entity_uid

    def to_json(self):
        return {"entity_uid": self.entity_uid, "symbol": self.symbol, "modifiers": self.modifiers}
