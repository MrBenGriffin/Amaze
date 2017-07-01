# encoding: utf-8
from tkinter import Canvas
from Maze.wall import Wall, Orientation
from Maze.cell import Cell
from Maze.cross import Cross


class Dim:
    def __init__(self, x=None, y=None, z=None):
        if not x:
            self.x = 0
        else:
            self.x = x
        if not y:
            self.y = 0
        else:
            self.y = y
        if not z:
            self.z = 0
        else:
            self.z = z

    def __repr__(self):
        return "%02x%02x%02x" % (self.x, self.y, self.z)

    def __str__(self):
        return "%02x\n%02x" % (self.x, self.y)

    def __cmp__(self, other):
        return self.x == other.x and self.y == other.y and self.z == other.z


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
        self.tk_maze = None
        self.bods = []
        self.levels = []
        # print("Making maze:", cells_across, cells_up, depth)
        for level in range(depth):
            floor = Level(cells_across, cells_up, cell_size, level)
            self.levels.append(floor)
        # Now we have all the levels we can add ceilings and floors to the cells.
        for level_index in range(depth):
            level = self.levels[level_index]
            up_layer = down_layer = None
            if level_index != depth - 1 and depth > 1:
                down_layer = self.levels[level_index + 1]
            if level_index != 0 and depth > 1:
                up_layer = self.levels[level_index - 1]
            for cell_across in range(self.cells_across):
                for cell_up in range(self.cells_up):
                    # if depth == 2 and level == 0, up is None and down is 1
                    # if depth == 2 and level == 1, up is 0 and down is None
                    level.cell(cell_across, cell_up).set_floor(up_layer, down_layer)

    def cell(self, cells_across, cells_up, level=None):
        if not level:
            return self.levels[0].cell(cells_across, cells_up)
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
    def __init__(self, cells_across, cells_up, cell_size, level):
        Cell.size = cell_size
        self.level = level
        self.tk_level = None
        self.cells_across = cells_across
        self.cells_up = cells_up

        self.ns_walls = [[
            Wall(Orientation.NS, i, j)
            for j in range(self.cells_up + 1)] for i in range(self.cells_across)]

        self.ew_walls = [[
            Wall(Orientation.EW, i, j)
            for j in range(self.cells_up)] for i in range(self.cells_across + 1)]

        self.cells = [[
            Cell(Dim(i, j, level), self.ns_walls, self.ew_walls)
            for j in range(self.cells_up)] for i in range(self.cells_across)]

    def cell(self, cells_across, cells_up):
        return self.cells[cells_across][cells_up]

    def tk_paint(self):
        for i in range(len(self.ns_walls)):
            for j in range(len(self.ns_walls[i])):
                self.ns_walls[i][j].tk_paint(self.tk_level)
        for i in range(len(self.ew_walls)):
            for j in range(len(self.ew_walls[i])):
                self.ew_walls[i][j].tk_paint(self.tk_level)
        for i in range(len(self.cells)):
            for j in range(len(self.cells[i])):
                self.cells[i][j].tk_paint(self.tk_level)

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
