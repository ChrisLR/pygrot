import pyglet
import copy


class JoystickMotion(object):
    THRESHOLD = 0.2
    MAX_SPEED_PER_TICK = 20

    def __init__(self, joystick):
        self.last_motions = 0, 0, 0, 0
        self.joystick = joystick

    def update(self, dt):
        motion = [self.joystick.x, self.joystick.y, self.joystick.rx, self.joystick.ry]
        speed_values = copy.copy(motion)
        for number, value in enumerate(self.last_motions):
            if motion[number] == value:
                speed_values[number] += value if not speed_values[number] + value > self.MAX_SPEED_PER_TICK else self.MAX_SPEED_PER_TICK
        self.last_motions = motion
        return speed_values


class Game(object):
    def __init__(self):
        self.player = None
        self.joysticks = None
        self.batch = None
        self.clock = None
        self.window = None
        self.initialize_ui()
        self.initialize_game()
        pyglet.clock.schedule_interval(self.update, 1 / 60.)
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

    def initialize_game(self):
        from spriteloader import SpriteLoader
        from monsters import Skeleton
        spriteloader = SpriteLoader()
        skeleton_template = Skeleton(spriteloader)
        for x in range(10):
            for y in range(10):
                skeleton = skeleton_template.create((x * 16, y * 16))
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

game = Game()

# @window.event
# def on_mouse_press(x, y, button, modifiers):
#     pass
#
#
# @window.event
# def on_mouse_release(x, y, button, modifiers):
#     pass








# @joystick.event
# def on_joybutton_press(joystick, button):
#     print("Button {} down".format(button))


# @joystick.event
# def on_joybutton_release(joystick, button):
#     print("Button {} up".format(button))


# @joystick.event
# def on_joyaxis_motion(joystick, axis, button):
#     if axis == 'y':
#         joystick_motion_y[0] = button
#     if axis == 'x':
#         joystick_motion_x[0] = button
#     if axis == 'ry':
#         joystick_motion_ry[0] = button
#     if axis == 'rx':
#         joystick_motion_rx[0] = button
#
#     print("Axis {} ".format(axis))




