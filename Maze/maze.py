# encoding: utf-8
from tkinter import Canvas
from Maze.wall import Wall, Orientation
from Maze.cell import Cell, Dim

"""
    Maze is created as a rectangle of x * y cells
"""


class Maze:
    def __init__(self, cells_across, cells_up, cell_size):
        Cell.size = cell_size
        self.cells_across = cells_across
        self.cells_up = cells_up
        self.tk_root = None
        self.tk_maze = None
        self.bods = []

        self.ns_walls = [[
            Wall(Orientation.NS, i, j)
            for j in range(self.cells_up + 1)] for i in range(self.cells_across)]

        self.ew_walls = [[
            Wall(Orientation.EW, i, j)
            for j in range(self.cells_up)] for i in range(self.cells_across + 1)]

        self.cells = [[
            Cell(Dim(i, j), self.ns_walls, self.ew_walls)
            for j in range(self.cells_up)] for i in range(self.cells_across)]

    def cell(self, cells_across, cells_up):
        return self.cells[cells_across][cells_up]

    def add_bod(self, bod, show):
        if show:
            self.bods.append(bod)
            bod.tk_init(self.tk_maze)
        else:
            while not bod.finished():
                bod.run()

    def tk_init(self, root):
        self.tk_root = root
        self.tk_root.title("Maze")
        self.tk_maze = Canvas(self.tk_root,
                              width=20 + Cell.size * (self.cells_across + 0),
                              height=20 + Cell.size * (self.cells_up + 0),
                              bg='gray')
        self.tk_maze.grid(columns=1, rows=1)
        self.tk_maze.after(0, self.animation)

    def tk_paint(self):
        for i in range(len(self.ns_walls)):
            for j in range(len(self.ns_walls[i])):
                self.ns_walls[i][j].tk_paint(self.tk_maze)
        for i in range(len(self.ew_walls)):
            for j in range(len(self.ew_walls[i])):
                self.ew_walls[i][j].tk_paint(self.tk_maze)

    def animation(self):
        for bod in self.bods:
            bod.tk_paint()
        self.tk_maze.after(60, self.animation)

    def __str__(self):  # __str__ method here is just for easy visualisation purposes.
        line = "\n"
        for i in range(self.cells_across):
            line += "%s" % self.ns_walls[i][self.cells_up]
        line += "┫\n"
        for j in reversed(range(self.cells_up)):  # reversed: print goes from top to bottom..
            for i in range(self.cells_across):
                line += "%s%s" % (self.ew_walls[i][j], self.cells[i][j])

            line += "%s\n" % self.ew_walls[self.cells_across][j]
            for i in range(self.cells_across):
                line += "%s" % self.ns_walls[i][j]

            line += "┫\n"
        return line
