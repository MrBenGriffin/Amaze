# encoding: utf-8
from typing import Optional
from tkinter import HIDDEN

from enum import Enum
from Maze.cell import Com, Cell

""""
    Not knowing anything about Python, here is a simple Wall class that
    should represent what we need to know about Walls.
    There are two aspects to a wall in general, one is which direction it is going in
    (north-south) or (west-east) - and then whether or not it has a doorway in it.

    I have also added a simple 'enum' class for Orientation. It's possibly a bit OTT.
    Likewise, a Com (compass) class used to represent compass points.
"""


class Orientation(Enum):
    NS = True
    EW = False


class Wall:
    # following statics are used for text-drawing.
    prev_ew = False

    solids = {
        Orientation.NS: (0, 0, 1, 0),
        Orientation.EW: (0, 1, 0, 0)
    }

    def __init__(self, orientation, x, y):
        self.canvas = None
        self.blocked = False
        self.id = None
        self.x = x
        self.y = y
        self.door = "▦"
        self.cells = {Com.N: None, Com.S: None, Com.E: None, Com.W: None}
        self.orientation = orientation

        self.solid = tuple(10 + Cell.size * i + Cell.size * j for i, j in zip(
            Wall.solids[self.orientation],
            (self.x, self.y, self.x, self.y)
        ))

    def make_door(self, cell, kind=None) -> Optional[Cell]:  # edges are None
        if not self.is_edge():
            if self.canvas:
                self.canvas.itemconfig(self.id, state=HIDDEN)
            if kind is None:
                self.door = " "
            else:
                self.door = kind
        other = self.other(cell)
        other.mined = True
        return other

    def make_solid(self):
        self.door = "▦"

    def is_solid(self) -> bool:
        return self.is_edge() or self.door == "▦"

    def set_cell(self, cell, com) -> None:
        self.cells[com] = cell

    def other(self, cell) -> Optional[Cell]:
        """ Edges have no cell on the other side, so will return None """
        if self.orientation == Orientation.NS:
            if self.cells[Com.N] == cell:
                return self.cells[Com.S]
            else:
                return self.cells[Com.N]
        else:
            if self.cells[Com.E] == cell:
                return self.cells[Com.W]
            else:
                return self.cells[Com.E]

    def is_edge(self) -> bool:  # If on the edge, then one of my wall cells will be None.
        if self.orientation == Orientation.NS:
            return (self.cells[Com.N] is None) or (self.cells[Com.S] is None)
        else:
            return (self.cells[Com.W] is None) or (self.cells[Com.E] is None)

    def can_be_dug(self) -> bool:
        if self.blocked or self.is_edge():
            return False
        if self.orientation == Orientation.NS:
            return (not self.cells[Com.N].mined) or (not self.cells[Com.S].mined)
        else:
            return (not self.cells[Com.W].mined) or (not self.cells[Com.E].mined)

    def tk_paint(self, canvas):
        if not self.canvas:
            self.canvas = canvas
        if self.is_solid():
            self.id = canvas.create_line(self.solid, width=2)
        else:
            self.id = canvas.create_line(self.solid, width=2, state=HIDDEN)

    def __repr__(self):
        return "[" + str(self) + "]"
