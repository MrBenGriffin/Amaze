# encoding: utf-8
from enum import Enum
from Maze.cross import Cross

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
    size = 20

    def __init__(self, dim, wns, wew):
        self.rune = None  # No rune on initialisation.
        self.dim = dim
        self.mined = False
        self.walls = {Com.N: wns[dim.x][dim.y + 1],
                      Com.E: wew[dim.x + 1][dim.y],
                      Com.S: wns[dim.x][dim.y],
                      Com.W: wew[dim.x][dim.y]}
        self.walls[Com.N].set_cell(self, Com.S)
        self.walls[Com.E].set_cell(self, Com.W)
        self.walls[Com.S].set_cell(self, Com.N)
        self.walls[Com.W].set_cell(self, Com.E)

    def set_mined(self):
        self.mined = True

    def is_mined(self) -> bool:
        return self.mined

    def name(self) -> str:
        return self.dim

    def exits(self) -> dict:
        dict_of_exits = {}
        for compass, wall in self.walls.items():
            if not wall.is_solid():
                dict_of_exits[compass] = wall
        return dict_of_exits

    def walls_that_can_be_dug(self) -> dict:
        dict_of_walls = {}
        for compass, wall in self.walls.items():
            if wall.can_be_dug():
                dict_of_walls[compass] = wall
        return dict_of_walls

    def make_door_in(self, com, kind=None):
        return self.walls[com].make_door(self, kind)

    def change_rune(self, the_rune=None):  # Accepts a rune if one is passed.
        result = self.rune
        self.rune = the_rune
        return result

    def str_nwn(self):
        right = bottom = left = top = False
        north_wall = self.walls[Com.N]
        west_wall = self.walls[Com.W]

        if north_wall:
            n_cell = north_wall.other(self)
            right = north_wall.is_solid()
            if n_cell and n_cell.walls[Com.W]:
                top = n_cell.walls[Com.W].is_solid()
        if west_wall:
            w_cell = west_wall.other(self)
            bottom = west_wall.is_solid()
            if w_cell and w_cell.walls[Com.N]:
                left = w_cell.walls[Com.N].is_solid()

        nw = Cross(top, left, bottom, right)
        if right:
            n = Cross.XLXR
        else:
            n = " "
        return nw.cross + n

    def str_sws(self):
        left = bottom = False
        right = self.walls[Com.S].is_solid()
        top = self.walls[Com.W].is_solid()
        w_cell = self.walls[Com.W].other(self)
        if w_cell:
            left = True
        return Cross(top, left, bottom, right).cross + Cross.XLXR

    def str_ne(self):
        return Cross(self.walls[Com.N].other(self) is not None,
                     self.walls[Com.N].is_solid(),
                     True,
                     False).cross

    def __cmp__(self, other):
        return self.dim.x == other.dim.x and self.dim.y == other.dim.y

    def __str__(self):  # Just draw what's on the floor.
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
