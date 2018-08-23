import socket
import spriteloader
import monsters
import pyglet


class UDPClient(object):
    IP = "127.0.0.1"
    PORT = 9000

    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def send(self, message):
        self.socket.sendto(message.encode('utf8'), (self.IP, self.PORT))


class GameClient(object):
    def __init__(self):
        self.client = UDPClient()
        self.entity_id = None

    def initialize(self):
        pyglet.clock.schedule_interval(update, 1 / 60.)

    def connect(self):
        pass

    def disconnect(self):
        pass

    def receive_update(self, entities):
        pass

    def send_input(self, symbol, modifiers):
        pass

    def internal_update(self):
        pass


if __name__ == '__main__':
    comm = NetworkComm(1, 2, 3, "KEK")
    dat_comm = NetworkSerializer(comm).data
    client = UDPClient()
    client.send(dat_comm)
