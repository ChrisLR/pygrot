from pygrot.client import game
from pygrot.netmessages.echoprotocol import Echo
from pygrot.netmessages import listing


class AbstractServer(object):
    def __init__(self, address):
        self.address = address


class GameClient(object):
    IP = "localhost"
    CLIENT_PORT = 9000
    SERVER_PORT = 9001

    def __init__(self, echo_protocol=None):
        self.message_handlers = {
            listing.JoinAccept: self.on_join_accepted,
            listing.KickNotification: self.on_kick_notification,
            listing.CompleteUpdate: self.on_complete_update
        }
        self.echo_protocol = Echo(self.CLIENT_PORT, self.IP, self.SERVER_PORT) if echo_protocol is None else echo_protocol
        self.entity_uid = None
        self.game = None
        self.server = None

    def start(self):
        self.echo_protocol.start()
        self.initialize_game()

    def on_join_accepted(self, message):
        uid = message.entity['uid']
        name = message.entity['name']
        position = message.entity['position']
        self.entity_uid = uid
        self.game.set_player_entity(uid, name, position)

    def on_kick_notification(self, message):
        pass

    def on_complete_update(self, message):
        pass

    def initialize_game(self):
        self.game = game.Game(self)
        self.connect()
        self.game.start()

    def connect(self):
        if not self.server:
            self.server = AbstractServer((self.IP, self.SERVER_PORT))
            message = listing.JoinRequest("")
            self.send((message,))

    def disconnect(self):
        if self.server:
            message = listing.DisconnectRequest("")
            self.send((message,))

    def update(self):
        remote_info, messages = self.echo_protocol.get()
        if remote_info is not None and messages is not None:
            self.handle_messages(remote_info, messages)

    def receive_update(self, entities):
        self.game.server_update(entities)

    def send_input(self, symbol, modifiers):
        if not self.entity_uid:
            return

        message = listing.KeyInput(symbol, modifiers, self.entity_uid)
        self.send((message,))

    def send(self, messages):
        self.echo_protocol.send(self.server, messages, "CLIENT")

    def handle_messages(self, info, messages):
        for message in messages:
            handler = self.message_handlers.get(type(message))
            if handler is None:
                print("Unhandled message " + str(message))
                continue
            handler(message)
