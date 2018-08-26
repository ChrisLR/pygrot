from networking.messages.base import BaseMessage, MessageCaspule
from networking.messages.client import ClientMessage, DisconnectRequest, JoinRequest, KeyInput
from networking.messages.server import ServerMessage, CompleteUpdate, JoinAccept, KickNotification


all_messages = (
    BaseMessage,
    MessageCaspule,
    ClientMessage,
    DisconnectRequest,
    JoinAccept,
    JoinRequest,
    KeyInput,
    ServerMessage,
    CompleteUpdate,
    KickNotification
)

message_mapping = {}
for i, message in enumerate(all_messages):
    message_mapping[i] = message
