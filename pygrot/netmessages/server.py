from pygrot.netmessages.base import BaseMessage


class ServerMessage(BaseMessage):
    pass


class JoinAccept(ServerMessage):
    type_no = 4

    def __init__(self, entity_id):
        super().__init__()
        self.entity_id = entity_id

    def to_json(self):
        return {"entity_id": self.entity_id}


class KickNotification(ServerMessage):
    type_no = 5

    def __init__(self, reason):
        super().__init__()
        self.reason = reason

    def to_json(self):
        return {"reason": self.reason}


class CompleteUpdate(ServerMessage):
    type_no = 6

    def __init__(self, entities):
        super().__init__()
        self.entities = entities

    def to_json(self):
        return {"reason": self.reason}
