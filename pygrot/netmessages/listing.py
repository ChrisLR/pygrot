from pygrot.netmessages.client import ClientMessage, DisconnectRequest, JoinRequest, KeyInput
from pygrot.netmessages.server import ServerMessage, CompleteUpdate, JoinAccept, KickNotification
from pygrot.netmessages.base import BaseMessage, MessageCapsule

all_messages = (
    BaseMessage,
    MessageCapsule,
    ClientMessage,
    DisconnectRequest,
    JoinAccept,
    JoinRequest,
    KeyInput,
    ServerMessage,
    CompleteUpdate,
    KickNotification
)

message_mapping = {message.type_no: message for message in all_messages}
