from networking.messages.base import BaseMessage


class ServerMessage(BaseMessage):
    pass


class JoinAccept(ServerMessage):
    def __init__(self, entity_id):
        super().__init__()
        self.entity_id = entity_id


class KickNotification(ServerMessage):
    def __init__(self, reason):
        super().__init__()
        self.reason = reason


class CompleteUpdate(ServerMessage):
    def __init__(self, entities):
        super().__init__()
        self.entities = entities
