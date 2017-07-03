# encoding: utf-8
from typing import Optional
from tkinter import HIDDEN
from Maze.cell import Cell
from Maze.util import Dim, Com, Orientation

""""
    Not knowing anything about Python, here is a simple Wall class that
    should represent what we need to know about Walls.
    There are two aspects to a wall in general, one is which direction it is going in
    (north-south) or (west-east) - and then whether or not it has a doorway in it.

    I have also added a simple 'enum' class for Orientation. It's possibly a bit OTT.
    Likewise, a Com (compass) class used to represent compass points.
"""


class Wall:
    # following statics are used for text-drawing.
    prev_ew = False

    solids = {
        Orientation.NS: (0, 0, 1, 0),
        Orientation.EW: (0, 1, 0, 0)
    }

    def __init__(self, orientation, x, y, level):
        self.level = level
        self.blocked = False
        self.id = None
        self.x = x
        self.y = y
        self.door = "▦"
        self.cells = {}
        # We need the orientation in order to draw the right wall..
        self.orientation = orientation

        self.solid = tuple(10 + Cell.size * i + Cell.size * j for i, j in zip(
            Wall.solids[self.orientation],
            (self.x, self.y, self.x, self.y)
        ))

    def make_door(self, cell_dir, kind=None):
        if cell_dir not in self.cells:
            return None
        other = self.cells[cell_dir]
        if not self.blocked and other:
            other.mined = True
            if self.level.tk_level:
                self.level.tk_level.itemconfig(self.id, state=HIDDEN)
            if kind is None:
                self.door = " "
            else:
                self.door = kind
            return other
        else:
            return None

    def make_solid(self):
        self.door = "▦"

    def is_solid(self) -> bool:
        return self.door == "▦"

    def set_cell(self, cell, com):
        self.cells[com] = cell
        opp = com.opposite
        if opp not in self.cells:
            self.cells[opp] = None

    def is_edge(self):  # If on the edge, then one of my wall cells will be None.
        if self.orientation == Orientation.NS:
            return (self.cells[Com.N] is None) or (self.cells[Com.S] is None)
        else:
            return (self.cells[Com.W] is None) or (self.cells[Com.E] is None)

    def can_be_dug(self, com_from):
        # if this is not blocked and there is a cell and it's not mined, self can be dug.
        cell = self.cells[com_from]
        return not self.blocked and cell and not cell.mined

    def tk_paint(self):
        if self.level.tk_level:
            if self.is_solid():
                self.id = self.level.tk_level.create_line(self.solid, width=2)
            else:
                self.id = self.level.tk_level.create_line(self.solid, width=2, state=HIDDEN)


class Floor:
    """
    Represents a 'floor' between two cells.
    The cell floor is the lower cell's ceiling.
    the Com.C is the cell that sees this as a ceiling.
    the Com.F is the cell that sees this as a floor.
    """
    def __init__(self, ceiling, floor, level):
        self.cells = {Com.C: ceiling, Com.F: floor}
        self.solid = True
        self.level = level
        self.tk_c = self.tk_f = None
        if ceiling:
            ceiling.floors[Com.C] = self
        floor.floors[Com.F] = self
        t = floor.walls[Com.N].solid
        b = floor.walls[Com.S].solid
        # get the dimensions of cells and construct the co-ordinates for drawing the stairs.
        # basically, x0,y0 x1,y1
        self.p = Dim(b[0] + 4, t[1] - 4, 0)
        self.q = Dim(b[2]-4, b[1] + 4, 0)

    def other(self, com):
        return self.cells[com.opposite]

    def make_hole(self, com):
        self.solid = False
        this = self.cells[com]
        other = self.other(com)
        if this:
            self.tk_paint(this)
        if other:
            self.tk_paint(other)
        return other

    def tk_paint(self, cell):
        if self.solid:
            return
        if self.level.tk_level:
            if cell == self.cells[Com.C]:
                self.tk_c = self.level.tk_level.create_line(
                    (self.p.x, self.p.y, self.q.x, self.p.y, self.q.x, self.q.y, self.p.x, self.p.y),
                    width=2, fill='red')
            elif cell == self.cells[Com.F]:
                self.tk_f = self.level.tk_level.create_line(
                    (self.p.x, self.p.y, self.p.x, self.q.y, self.q.x, self.p.y, self.p.x, self.p.y),
                    width=2, fill='blue')
