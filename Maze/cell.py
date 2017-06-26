# encoding: utf-8
from enum import Enum
from tkinter import Canvas

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
    lo = 0
    hi = 20
    solids = {
        Com.N: (hi, hi, lo, hi),  # TK is weird. 0,0 is at the TOP left of the screen.
        Com.W: (lo, hi, lo, lo),  # So we are going to have to rotate our stuff 180°
        Com.S: (lo, lo, hi, lo),
        Com.E: (hi, lo, hi, hi)
    }

    def __init__(self, dim, wns, wew):
        self.rune = None  # No rune on initialisation.
        self.mined = None
        self.dim = dim
        self.walls = {Com.N: wns[dim.x][dim.y + 1],
                      Com.E: wew[dim.x + 1][dim.y],
                      Com.S: wns[dim.x][dim.y],
                      Com.W: wew[dim.x][dim.y]}
        """"
        OMG all back to front. 
        So, my wall to the North, sees me as being in the South, right?
        etc. etc.
        """
        self.walls[Com.N].set_cell(self, Com.S)
        self.walls[Com.E].set_cell(self, Com.W)
        self.walls[Com.S].set_cell(self, Com.N)
        self.walls[Com.W].set_cell(self, Com.E)

    def name(self):
        return self.dim

    def set_mined(self, dim):
        self.mined = dim

    def get_mined(self):
        return self.mined

    def exits(self):
        result = {}
        for key, wall in self.walls.items():
            if not wall.is_solid():
                result[key] = wall
        return result

    def digs(self):
        result = {}
        for key, wall in self.walls.items():
            if wall.can_be_dug():
                result[key] = wall
        return result

    def make_door(self, com, kind=None):
        return self.walls[com].make_door(self, kind)

    def change_rune(self, the_rune=None):  # Returns any key currently here. Accepts a key if one is passed.
        result = self.rune
        self.rune = the_rune
        return result

    def tk_draw(self, parent):     # This method is really quite slow when dealing with lots of cells.
        canvas = Canvas(parent, width=20, height=20, highlightthickness=0)
        for key, wall in self.walls.items():
            if wall.is_solid():
                canvas.create_line(self.solids[key], width=3)
                canvas.create_text(8, 11, text=self.dim, font=("Courier", 8), fill="gray")
        return canvas

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

    def __repr__(self):
        return "%02x%02x" % (self.x, self.y)

    def __str__(self):
        return "%02x\n%02x" % (self.x, self.y)
