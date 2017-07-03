# encoding: utf-8
from tkinter import Canvas
from Maze.util import Orientation, Dim
from Maze.wall import Wall, Floor
from Maze.cell import Cell
from Maze.cross import Cross


class Maze:
    """
        Maze is created as a rectangle (cuboid) of x * y (*z) cells.

        Each Maze is made of 1...X levels.
        Each Maze level has it's own Canvas..
        For the time being, each level uses the same dimensions..
        (Not hard to change this).

    """
    def __init__(self, cells_across, cells_up, depth, cell_size):
        self.cells_across = cells_across
        self.cells_up = cells_up
        self.depth = depth
        self.tk_maze = None
        self.bods = []
        self.levels = []
        # print("Making maze:", cells_across, cells_up, depth)
        for level in range(self.depth):
            floor = Level(self, cells_across, cells_up, cell_size, level)
            self.levels.append(floor)

    def cell(self, cells_across, cells_up, level=None):
        if level is None or level < 0:
            return None
        return self.levels[level].cell(cells_across, cells_up)

    def add_bod(self, bod, show):
        if show and self.tk_maze:
            self.bods.append(bod)
            bod.tk_init(self.levels)
        else:
            while not bod.finished():
                bod.run()

    def tk_init(self, root):
        self.tk_maze = root
        self.tk_maze.title("Maze")
        for level in self.levels:
            level.tk_level = Canvas(self.tk_maze,
                                    width=20 + Cell.size * (self.cells_across + 0),
                                    height=20 + Cell.size * (self.cells_up + 0),
                                    bg='gray')
            level.tk_level.grid(columns=1, rows=1)
        self.tk_maze.after(0, self.animation)

    def animation(self):
        for bod in self.bods:
            bod.tk_paint()
        self.tk_maze.after(60, self.animation)

    def tk_paint(self):
        for level in self.levels:
            level.tk_paint()

    def __str__(self):
        result = ""
        for level in self.levels:
            result += str(level)
        return result


class Level:
    def __init__(self, maze, cells_across, cells_up, cell_size, level):
        Cell.size = cell_size
        self.level = level
        self.tk_level = None
        self.cells_across = cells_across
        self.cells_up = cells_up

        self.ns_walls = [[
            Wall(Orientation.NS, i, j, self)
            for j in range(self.cells_up + 1)] for i in range(self.cells_across)]

        self.ew_walls = [[
            Wall(Orientation.EW, i, j, self)
            for j in range(self.cells_up)] for i in range(self.cells_across + 1)]

        self.cells = [[
            Cell(Dim(i, j, level), self.ns_walls, self.ew_walls)
            for j in range(self.cells_up)]
            for i in range(self.cells_across)]

        self.floors = [[
            Floor(maze.cell(i, j, self.level - 1), self.cells[i][j], self)
            for j in range(self.cells_up)]
            for i in range(self.cells_across)]

    def cell(self, cells_across, cells_up):
        return self.cells[cells_across][cells_up]

    def tk_paint(self):
        for i in range(len(self.ns_walls)):
            for j in range(len(self.ns_walls[i])):
                self.ns_walls[i][j].tk_paint()
        for i in range(len(self.ew_walls)):
            for j in range(len(self.ew_walls[i])):
                self.ew_walls[i][j].tk_paint()
        for i in range(len(self.cells)):
            for j in range(len(self.cells[i])):
                self.floors[i][j].tk_paint(self.cells[i][j])

    def __str__(self):  # __str__ method here is just for easy visualisation purposes.
        line = "Level %s\n" % (1 + self.level)
        for j in reversed(range(self.cells_up)):  # reversed: print goes from top to bottom..
            for i in range(self.cells_across):
                line += self.cell(i, j).str_nwn()
            line += self.cell(self.cells_across - 1, j).str_ne()
            line += "\n"
        for i in range(self.cells_across):
            line += self.cell(i, 0).str_sws()
        line += Cross.TLXX + "\n"
        return line
