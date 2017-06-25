# encoding: utf-8
from enum import Enum
from Maze.cell import Com

""""
    Not knowing anything about Python, here is a simple Wall class that
    should represent what we need to know about Walls.
    There are two aspects to a wall in general, one is which direction it is going in
    (north-south) or (west-east) - and then whether or not it has a doorway in it.

    I have also added a simple 'enum' class for Orientation. It's possibly a bit OTT.
    Likewise, a Com (compass) class used to represent compass points.
"""


class Wall:
    """
    Huh?, you may well ask. what is self.cells and how does a wall relate to four cells?!
    In brief, it's the cells either side of the wall, and two will remain undefined.
    So, we are currently using a grid/2d-array of cells..
    But each wall is in another array, so that we can share walls with cells.

    +-----+-----+--- <--- N for row 1, S for row 2
    | 0,1 | 1,1 | 2,1
    |<W E>|<W E>|<--west
    +-----+-----+--  <--- N for row 0, S for row 1
    | 0,0 | 1,0 | 2,0
    |<W E>|<W E>|<--east
    +-----+-----+--  <--- No.N (edge), S for row 0.

    Now all of this may be one complete waste of time..
    All I am trying to do is to find a way of capturing the basic structure of a maze...
    """

    def __init__(self, orientation=None, kind=None):
        self.cells = {Com.N: None, Com.S: None, Com.E: None, Com.W: None}
        if orientation is None:
            self.orientation = Orientation.NS
        else:
            self.orientation = orientation

        if kind is None:
            self.make_solid()
        else:
            self.door = kind

    def make_door(self, kind=None):  # There is no edge escape from the Maze...
        if not self.is_edge():
            if kind is None:
                self.door = " "
            else:
                self.door = kind

    def make_solid(self):
        if self.orientation == Orientation.NS:
            self.door = "━"
        else:
            self.door = "┃"

    def is_solid(self):
        return self.door == "━" or self.door == "┃"

    def set_cell(self, cell, com):
        self.cells[com] = cell

    def is_edge(self):  # If on the edge, then one of my wall cells will be None.
        if self.orientation == Orientation.NS:
            return (self.cells[Com.N] is None) or (self.cells[Com.S] is None)
        else:
            return (self.cells[Com.W] is None) or (self.cells[Com.E] is None)

    def __str__(self):
        return self.door

    def __repr__(self):
        return "[" + self.door + "]"


class Orientation(Enum):
    NS = True
    EW = False
