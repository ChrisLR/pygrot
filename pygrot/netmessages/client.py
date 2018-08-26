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

    def __init__(self, symbol, modifiers, username):
        super().__init__()
        self.symbol = symbol
        self.modifiers = modifiers
        self.username = username

    def to_json(self):
        return {"username": self.username, "symbol": self.symbol, "modifiers": self.modifiers}
