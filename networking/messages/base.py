import json
from socket import gethostname


class BaseMessage(object):
    pass


class MessageCaspule(object):
    def __init__(self, messages, sender):
        self.messages = messages
        self.sender = sender

    @classmethod
    def create(cls, messages):
        return MessageCaspule(messages, gethostname())

    @classmethod
    def from_json(cls, messages, sender):
        return MessageCaspule(messages, sender)

    def to_json(self):
        json_messages = {message.type_no: message.to_json() for message in self.messages}
        json_message = {"sender": self.sender, "messages": json_messages}

        return json.dumps(json_message)
