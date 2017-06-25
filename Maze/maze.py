# encoding: utf-8
from wall import Wall, Orientation
from cell import Cell, Dim

"""
    Maze is created as a rectangle of x * y cells
"""


class Maze:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.ns_walls = [[Wall(Orientation.NS) for i in range(self.y + 1)] for j in range(self.x)]
        self.ew_walls = [[Wall(Orientation.EW) for i in range(self.y)] for j in range(self.x + 1)]
        self.cells = [[Cell(Dim(i, j), self.ns_walls, self.ew_walls) for j in range(self.y)] for i in range(self.x)]

    def make_door(self, x, y, com, kind=None):
        self.cells[x][y].make_door(com, kind)

    def change_rune(self, x, y, the_rune=None):
        return self.cells[x][y].change_rune(the_rune)

    def exits(self, x, y):  # Given a cell (as x,y), return all the exits available.
        return self.cells[x][y].exits()

    def __str__(self):   # __str__ method here is just for easy visualisation purposes.
        line = "\n"
        for i in range(self.x):
            line += "╋%s" % self.ns_walls[i][self.y]
        line += "╋\n"
        for j in reversed(range(self.y)):  # reversed because we are printing, and print goes from top to bottom..
            for i in range(self.x):
                line += "%s%s" % (self.ew_walls[i][j], self.cells[i][j])

            line += "%s\n" % self.ew_walls[self.x][j]
            for i in range(self.x):
                line += "╋%s" % self.ns_walls[i][j]

            line += "╋\n"
        return line
