from pygrot.client import game
from twisted.internet import reactor
from pygrot.netmessages.echoprotocol import Echo
from pygrot.netmessages import listing


class AbstractServer(object):
    def __init__(self, address):
        self.address = address


class GameClient(object):
    IP = "127.0.0.1"
    CLIENT_PORT = 9000
    SERVER_PORT = 9001

    def __init__(self):
        self.message_handlers = {
            listing.JoinAccept: self.on_join_accepted,
            listing.KickNotification: self.on_kick_notification,
            listing.CompleteUpdate: self.on_complete_update
        }
        self.echo_protocol = Echo()
        self.entity_id = None
        self.game = None
        self.server = None
        reactor.callInThread(self.initialize_game)
        self.listen()

    def on_join_accepted(self, message):
        uid = message.uid
        name = message.name
        position = message.position
        self.entity_id = uid
        self.game.set_player_entity(uid, name, position)

    def on_kick_notification(self, message):
        pass

    def on_complete_update(self, message):
        pass

    def initialize_game(self):
        self.game = game.Game(self)
        self.connect()

    def connect(self):
        if not self.server:
            self.server = AbstractServer((self.IP, self.SERVER_PORT))
            message = listing.JoinRequest("")
            self.send((message,))

    def disconnect(self):
        if self.server:
            message = listing.DisconnectRequest("")
            self.send((message,))

    def receive_update(self, entities):
        pass

    def send_input(self, symbol, modifiers):
        if not self.entity_id:
            return

        message = listing.KeyInput(symbol, modifiers, self.entity_id)
        self.send((message,))

    def send(self, messages):
        self.echo_protocol.send(self.server, messages, "CLIENT")

    def handle_messages(self, info, messages):
        for message in messages:
            handler = self.message_handlers.get(message)
            if handler is None:
                print("Unhandled message " + str(message))
                continue
            handler(message)

    def listen(self):
        reactor.listenUDP(self.CLIENT_PORT, self.echo_protocol)
        reactor.run()
