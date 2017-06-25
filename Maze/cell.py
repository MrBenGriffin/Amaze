# encoding: utf-8

"""
    Dim represents an integer x,y dimension.
    Typically this is something that one would find in a two dimensional array.

    Cell is a single cell (or room) of the maze.. It has four walls, referring to the wall class.
    Most cell-walls are shared by neighbouring cells.

    A cell is initialised with it's dimension (x/y values) and access to the (ns/ew) walls arrays.
"""


class Dim:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def show(self):
        return "(%s, %s)" % (self.x, self.y)


class Cell:
    def __init__(self, dim, wns, wew):
        self.dim = dim
        self.n = wns[dim.x][dim.y+1]
        self.s = wns[dim.x][dim.y]
        self.e = wew[dim.x+1][dim.y]
        self.w = wew[dim.x][dim.y]
        self.n.set_cell(self, True)
        self.s.set_cell(self, False)
        self.e.set_cell(self, True)
        self.w.set_cell(self, False)

