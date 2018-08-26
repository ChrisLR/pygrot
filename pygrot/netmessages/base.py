import abc
import json
from socket import gethostname


class BaseMessage(object):
    @property
    @abc.abstractmethod
    def type_no(self):
        raise NotImplementedError()


class MessageCapsule(BaseMessage, metaclass=abc.ABCMeta):
    type_no = 1

    def __init__(self, messages, sender):
        self.messages = messages
        self.sender = sender

    @classmethod
    def create(cls, messages):
        return MessageCapsule(messages, gethostname())

    def to_json(self):
        json_messages = [{"type_no": message.type_no, "message": message.to_json()}
                         for message in self.messages]
        json_message = {"sender": self.sender, "netmessages": json_messages}

        return json.dumps(json_message)
