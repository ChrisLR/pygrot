from pygrot.netmessages.base import BaseMessage


class ServerMessage(BaseMessage):
    pass


class JoinAccept(ServerMessage):
    type_no = 4

    def __init__(self, entity):
        super().__init__()
        self.entity = entity

    def to_json(self):
        return {"entity": {"uid": self.entity.uid, "name": self.entity.name, "position": self.entity.position}}


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
        return {"entities": {entity.uid: self.entity_as_json(entity) for entity in self.entities.values()}}

    def entity_as_json(self, entity):
        return {"uid": entity.uid, "name": entity.name, "position": entity.position}
