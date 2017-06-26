# encoding: utf-8
from enum import Enum

"""
    Dim represents an integer x,y dimension.
    Typically this is something that one would find in a two dimensional array.

    Cell is a single cell (or room) of the maze.. It has four walls, referring to the wall class.
    Most cell-walls are shared by neighbouring cells.

    A cell is initialised with it's dimension (x/y values) and access to the (ns/ew) walls arrays.
"""


class Com(Enum):
    N = 'N'
    S = 'S'
    E = 'E'
    W = 'W'


class Cell:
    def __init__(self, dim, wns, wew):
        self.rune = None  # No rune on initialisation.
        self.mined = None
        self.dim = dim
        self.walls = {Com.N: wns[dim.x][dim.y + 1],
                      Com.S: wns[dim.x][dim.y],
                      Com.E: wew[dim.x + 1][dim.y],
                      Com.W: wew[dim.x][dim.y]}
        """"
        OMG all back to front. 
        So, my wall to the North, sees me as being in the South, right?
        etc. etc.
        """
        self.walls[Com.N].set_cell(self, Com.S)
        self.walls[Com.S].set_cell(self, Com.N)
        self.walls[Com.E].set_cell(self, Com.W)
        self.walls[Com.W].set_cell(self, Com.E)

    def name(self):
        return self.dim

    def set_mined(self, dim):
        self.mined = dim

    def get_mined(self):
        return self.mined

    def exits(self):
        exits = {}
        for key, wall in self.walls.items():
            if not wall.is_solid():
                exits[key] = wall
        return exits

    def digs(self):
        digs = {}
        for key, wall in self.walls.items():
            if wall.can_be_dug():
                digs[key] = wall
        return digs

    def make_door(self, com, kind=None):
        return self.walls[com].make_door(self, kind)

    def change_rune(self, the_rune=None):    # Returns any key currently here. Accepts a key if one is passed.
        result = self.rune
        self.rune = the_rune
        return result

    def __cmp__(self, other):
        return self.dim.x == other.dim.x and self.dim.y == other.dim.y

    def __str__(self):  # Just draw what's on the floor. Walls draw themselves.
        if self.rune is None:
            return " "
        return self.rune


class Dim:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return "(%s, %s)" % (self.x, self.y)



