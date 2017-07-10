# encoding: utf-8
from enum import Enum, IntFlag


# Decorator class.
class Reverse:
    def __init__(self, reverse_map):
        self.reverse_map = reverse_map

    def __call__(self, enum):
        for fwd, rev in self.reverse_map.items():
            enum[fwd].opposite = enum[rev]
            enum[rev].opposite = enum[fwd]
        return enum


@Reverse({'N': 'S', 'E': 'W', 'C': 'F', "NW": "SE", "NE": "SW"})
class Com(IntFlag):
    X = 0x0000
    W = 0x0001
    E = 0x0002
    N = 0x0004
    S = 0x0008
    C = 0x0010
    F = 0x0020
    SW = 0x0040
    NE = 0x0080
    NW = 0x0100
    SE = 0x0200


class Orientation(Enum):
    NS = True
    EW = False


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

    def __str__(self):
        return "%02x\n%02x" % (self.x, self.y)

    def __cmp__(self, other):
        return self.x == other.x and self.y == other.y and self.z == other.z


if __name__ == "__main__":
    print(Com.N | Com.S)
    print(Com.W)
    print(Com.N.opposite)
    print((Com.W | Com.E | Com.N))
    print(Com.W | Com.E)
    print(Com.C)
    print(Com.C.opposite)
