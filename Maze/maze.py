# encoding: utf-8
from Maze.wall import Wall, Orientation
from Maze.cell import Cell, Dim

"""
    Maze is created as a rectangle of x * y cells
"""


class Maze:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.ns_walls = [[
            Wall(Orientation.NS, i, j)
            for j in range(self.y + 1)] for i in range(self.x)]

        self.ew_walls = [[
            Wall(Orientation.EW, i, j)
            for j in range(self.y)] for i in range(self.x + 1)]

        self.cells = [[
            Cell(Dim(i, j), self.ns_walls, self.ew_walls)
            for j in range(self.y)] for i in range(self.x)]

    def cell(self, x, y) -> Cell:
        return self.cells[x][y]

    def tk_paint(self, canvas):
        for i in range(len(self.ns_walls)):
            for j in range(len(self.ns_walls[i])):
                self.ns_walls[i][j].tk_paint(canvas)
        for i in range(len(self.ew_walls)):
            for j in range(len(self.ew_walls[i])):
                self.ew_walls[i][j].tk_paint(canvas)

    def __str__(self):  # __str__ method here is just for easy visualisation purposes.
        line = "\n"
        for i in range(self.x):
            line += "╋%s" % self.ns_walls[i][self.y]
        line += "╋\n"
        for j in reversed(range(self.y)):  # reversed: print goes from top to bottom..
            for i in range(self.x):
                line += "%s%s" % (self.ew_walls[i][j], self.cells[i][j])

            line += "%s\n" % self.ew_walls[self.x][j]
            for i in range(self.x):
                line += "╋%s" % self.ns_walls[i][j]

            line += "╋\n"
        return line
