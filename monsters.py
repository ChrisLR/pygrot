import pyglet
import character
import random


class Monster(object):
    name = ""
    frame_0_opts = ("", "", 0, 0)
    frame_1_opts = ("", "", 0, 0)

    def __init__(self, spriteloader):
        self.spriteloader = spriteloader
        self.animation = self._set_animations(spriteloader)

    def _set_animations(self, spriteloader):
        frames = []
        for sheet_name, name, row, col in (self.frame_0_opts, self.frame_1_opts):
            sheet = spriteloader.get_by_name(sheet_name)
            sheet.set_region_name(name, row, col)
            frame = pyglet.image.AnimationFrame(sheet.get_region_by_name(name), 0.1)
            frames.append(frame)

        return pyglet.image.Animation(frames)

    def create(self, location):
        animations = character.Animations()
        animations.add("idle", self.animation)
        new_character = character.GameObject(
            name=self.name,
            animations=animations,
            location=character.Location(*location),
            properties=character.Properties()
        )

        return new_character


class Skeleton(Monster):
    name = "Skeleton"
    frame_0_opts = ("Undead0", "skeleton", 7, 0)
    frame_1_opts = ("Undead1", "skeleton", 7, 0)
