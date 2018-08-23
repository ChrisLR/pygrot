from networking.messages.base import BaseMessage


class ClientMessage(BaseMessage):
    pass


class DisconnectRequest(ClientMessage):
    def __init__(self, username):
        super().__init__()
        self.username = username


class JoinRequest(ClientMessage):
    def __init__(self, username):
        super().__init__()
        self.username = username


class KeyInput(ClientMessage):
    def __init__(self, symbol, modifiers):
        super().__init__()
        self.symbol = symbol
        self.modifiers = modifiers
