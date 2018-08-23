import pyglet


class GameObject(object):
    def __init__(self, name, animations, location, properties):
        self.name = name
        self.animations = animations
        animations.host = self
        self.location = location
        self.properties = properties
        self.move_to = None

    def update(self):
        self.animations.current.position = self.location.tuple()
        if self.move_to:
            x, y = self.location.tuple()
            mx, my = self.move_to
            step_x, step_y = x - mx, y - my
            if step_x >= 4:
                step_x = 4
            elif step_x <= -4:
                step_x = -4
            if step_y >= 4:
                step_y = 4
            elif step_y <= -4:
                step_y = -4
            self.location.x -= step_x
            self.location.y -= step_y

        if self.move_to == self.location.tuple():
            self.move_to = None



class Animations(object):
    def __init__(self):
        self._animations = {}
        self.current = None
        self.sprite = None
        self.host = None

    def add(self, name, animation):
        self._animations[name] = animation

    def play(self, name, batch, group):
        animation = self._animations.get(name)
        if animation is not None:
            self.current = pyglet.sprite.Sprite(animation, batch=batch, group=group)
            self.current.position = self.host.location.tuple()
            self.current.scale = 1.5


class Location(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def tuple(self):
        return self.x, self.y


class Properties(object):
    def __init__(self, blocking=True):
        self.blocking = blocking
