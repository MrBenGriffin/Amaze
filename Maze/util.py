# encoding: utf-8
from enum import Enum


class Reverse:
    def __init__(self, reverse_map):
        self.reverse_map = reverse_map

    def __call__(self, enum):
        for first, second in self.reverse_map.items():
            enum[first].opposite = enum[second]
            enum[second].opposite = enum[first]
        return enum


class Orientation(Enum):
    NS = True
    EW = False


@Reverse({'N': 'S', 'E': 'W', 'C': 'F'})
class Com(Enum):
    N = 'N'  # North
    S = 'S'  # South
    E = 'E'  # East
    W = 'W'  # West
    C = 'C'  # Ceiling
    F = 'F'  # Floor


class Dim:
    def __init__(self, x=None, y=None, z=None):
        if not x:
            self.x = 0
        else:
            self.x = x
        if not y:
            self.y = 0
        else:
            self.y = y
        if not z:
            self.z = 0
        else:
            self.z = z

    # def __repr__(self):
    #     return "%02x%02x%02x" % (self.x, self.y, self.z)

    def __str__(self):
        return "%02x\n%02x" % (self.x, self.y)

    def __cmp__(self, other):
        return self.x == other.x and self.y == other.y and self.z == other.z
