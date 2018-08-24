import socket
import threading
import game
from twisted.internet import reactor
from networking.twistedudp import Listen


class UDPClient(object):
    IP = "127.0.0.1"
    CLIENT_PORT = 9000
    SERVER_PORT = 9001

    def __init__(self):
        self.datagram_protocol = Listen(self)

    def handle_message(self, data, host, port):
        print("I should do some shit here")

    def listen(self):
        reactor.listenUDP(self.CLIENT_PORT, self.datagram_protocol)
        reactor.run()

    def send(self, message):
        self.datagram_protocol.transport.write(message, (self.IP, self.SERVER_PORT))


class GameClient(object):
    def __init__(self):
        self.client = UDPClient()
        self.entity_id = None
        self.game = None
        reactor.callInThread(self.initialize)
        self.client.listen()

    def initialize(self):
        self.game = game.Game(self)
        self.client.send("KEK")

    def connect(self):
        pass

    def disconnect(self):
        pass

    def receive_update(self, entities):
        pass

    def send_input(self, symbol, modifiers):
        self.client.send("TEST".encode("utf-8"))
