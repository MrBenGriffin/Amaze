# encoding: utf-8
from enum import Enum

""""
    Not knowing anything about Python, here is a simple Wall class that
    should represent what we need to know about Walls.
    There are two aspects to a wall in general, one is which direction it is going in
    (north-south) or (west-east) - and then whether or not it has a doorway in it.

    I have also added a simple 'enum' class for Orientation. It's possibly a bit OTT.
    Likewise, a Com (compass) class used to represent compass points.
"""


class Wall:
    def __init__(self, orientation=None, has_door=None):
        if has_door is None:
            self.door = False
        else:
            self.door = has_door

        if orientation is None:
            self.orientation = Orientation.NS
        else:
            self.orientation = orientation

        self.cell_high = None
        self.cell_low = None

    def make_door(self):
        self.door = True

    def make_solid(self):
        self.door = False

    def set_cell(self, cell, high):  # relationN and E are high (true), S and W are low (false)
        if high:
            self.cell_high = cell
        else:
            self.cell_low = cell

    def __str__(self):
        if self.orientation == Orientation.NS:
            if self.door:
                return " "
            else:
                return "━"
        else:
            if self.door:
                return " "
            else:
                return "┃"


class Com(Enum):
    N = 1
    S = 2
    E = 3
    W = 4


class Orientation(Enum):
    NS = True
    EW = False

