import pyglet

from pygrot.client.input.joystick import JoystickMotion
from pygrot.client.graphics.spriteloader import SpriteLoader
from pygrot.gamedata.monsters import Skeleton


class Game(object):
    def __init__(self, client):
        self.client = client
        self.player = None
        self.joysticks = None
        self.batch = None
        self.clock = None
        self.window = None
        self.spriteloader = SpriteLoader()
        self.entities = {}

    def start(self):
        self.initialize_ui()
        pyglet.clock.schedule_interval(self.update, 1 / 60)
        pyglet.app.run()

    def on_draw(self):
        self.window.clear()
        self.batch.draw()
        self.clock.draw()

    def on_key_press(self, symbol, modifiers):
        if not self.player or not self.player.move_to:
            self.client.send_input(symbol, modifiers)

    def set_player_entity(self, uid, name, position):
        skeleton = self.spawn_entity(uid, name, position)
        self.player = skeleton

    def spawn_entity(self, uid, name, position):
        # TODO This is not always skeleton, but hey, baby steps
        skeleton_template = Skeleton(self.spriteloader)
        skeleton = skeleton_template.create(position)
        skeleton.animations.play("idle", self.batch, None)
        skeleton.uid = uid
        self.entities[uid] = skeleton

        return skeleton

    def initialize_ui(self):
        self.batch = pyglet.graphics.Batch()
        self.clock = pyglet.clock.ClockDisplay(interval=1.0 / 60.0)
        self.window = pyglet.window.Window()
        self.window.event(self.on_draw)
        self.window.event(self.on_key_press)

    def initialize_joysticks(self):
        joysticks = pyglet.input.get_joysticks()
        if joysticks:
            joystick = joysticks[0]
            joystick.open()
            joystick_motion_x = [0]
            joystick_motion_y = [0]
            joystick_motion_rx = [0]
            joystick_motion_ry = [0]
            joysticky = JoystickMotion(joystick)

    def update(self, dt):
        self.client.update()
        if self.player:
            self.player.update()

    def server_update(self, remote_entities):
        for remote_entity in remote_entities.values():
            if remote_entity.uid in self.entities:
                local_entity = self.entities.get(remote_entity.uid)
                if local_entity.location.tuple() != remote_entity.position:
                    local_entity.move_to = remote_entity.position
            else:
                self.spawn_entity(remote_entity.uid, remote_entity.name, remote_entity.position)
