import pyglet
from character import GameObject


class Floor(object):
    name = ""
    center_pos = (0, 0)
    # This mapping represent the offsets for the tiles in the sprite sheet
    _mapping = {
        "nw": (-1, 1),
        "n": (0, 1),
        "ne": (1, 1),
        "e": (1, 0),
        "se": (1, -1),
        "s": (0, -1),
        "sw": (-1, -1),
        "w": (-1, 0),
        "center": (0, 0),
        "v_top": (2, 1),
        "v_mid": (2, 0),
        "v_bot": (2, -1),
        "h_left": (3, 0),
        "h_mid": (4, 0),
        "h_right": (5, 0),
        "single": (4, 1),
    }

    def __init__(self, spriteloader):
        self.spriteloader = spriteloader
        self.sheet = spriteloader.get_by_name("Floor")
        self.sprites = {
            name: self.sheet.get_region(
                self.offset(self.center_pos, name)
            )
            for name in self._mapping.keys()
        }

    def offset(self, center, name):
        cx, cy = center
        ox, oy = self._mapping.get(name)

        return cx + ox, cy + oy

    def get_align(self, position, map):
        px, py = position


    def is_nw(self, position, map):
        required = {
            "nw": False,
            "n": False,
            "ne": False,
            "e" : True,
            "se": True,
            "s": True,
            "sw": False,
            "w": False,
        }
        tiles = {
           name: map.get_tile(self.offset(position, name))
            for name in self._mapping.keys()
        }
        return all([
            required.get(name) == tiles.get(name)
            for name in tiles.keys()
        ])

    def create(self, position, map, batch, group):
        pass
