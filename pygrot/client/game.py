import pyglet

from pygrot.client.input.joystick import JoystickMotion


class Game(object):
    def __init__(self, client):
        self.client = client
        self.player = None
        self.joysticks = None
        self.batch = None
        self.clock = None
        self.window = None
        self.initialize_ui()
        self.initialize_game()
        pyglet.clock.schedule_interval(self.update, 1 / 60)
        pyglet.app.run()

    def on_draw(self):
        self.window.clear()
        self.batch.draw()
        self.clock.draw()

    def on_key_press(self, symbol, modifiers):
        if not self.player.move_to:
            px, py = self.player.location.tuple()
            if symbol == pyglet.window.key.LEFT:
                self.player.move_to = px - 16, py
            if symbol == pyglet.window.key.UP:
                self.player.move_to = px, py + 16
            if symbol == pyglet.window.key.RIGHT:
                self.player.move_to = px + 16, py
            if symbol == pyglet.window.key.DOWN:
                self.player.move_to = px, py - 16

        self.client.send_input(symbol, modifiers)

    def initialize_game(self):
        from pygrot.client.graphics.spriteloader import SpriteLoader
        from pygrot.gamedata.monsters import Skeleton
        spriteloader = SpriteLoader()
        skeleton_template = Skeleton(spriteloader)
        skeleton = skeleton_template.create((16, 16))
        skeleton.animations.play("idle", self.batch, None)
        self.player = skeleton

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
        self.player.update()