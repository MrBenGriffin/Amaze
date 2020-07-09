from Maze.util import Orientation, Com, Dim
from Maze.wall import Wall, Floor, Corner
from Maze.cell import Cell

class Level:
    def __init__(self, maze, cells_across, cells_up, cell_size, level):
        Cell.size = cell_size
        self.maze = maze
        self.level = level
        self.tk_level = None
        self.cells_across = cells_across
        self.cells_up = cells_up
        self.floors = []

        self.ns_walls = [[
            Wall(Orientation.NS, i, j, self)
            for j in range(self.cells_up + 1)] for i in range(self.cells_across)]

        self.ew_walls = [[
            Wall(Orientation.EW, i, j, self)
            for j in range(self.cells_up)] for i in range(self.cells_across + 1)]

        self.cells = [[
            Cell(Dim(i, j, level), self.ns_walls, self.ew_walls, self)
            for j in range(self.cells_up)]
            for i in range(self.cells_across)]

        # Corner is top left of each cell.
        # So at cell 0,0 the corner sees the ns wall 0,0 as being East... +
        self.corners = [[
            Corner({Com.N: self._ew_wall(i, j - 1), Com.W: self._ns_wall(i - 1, j),
                    Com.S: self._ew_wall(i, j), Com.E: self._ns_wall(i, j)})
            for j in range(self.cells_up+1)]
            for i in range(self.cells_across+1)]

    def erode(self):
        for j in range(self.cells_up):
            for i in range(self.cells_across):
                self.cells[i][j].calc_values()
        # for wall in self.ns_walls:
        #     wall.erode()
        # for wall in self.ew_walls:
        #     wall.erode()

    def set_floor(self, maze):
        self.floors = [[Floor(self.cells[i][j], maze.cell(i, j, self.level + 1))
                       for j in range(self.cells_up)]
                       for i in range(self.cells_across)]

    def _ns_wall(self, across, up):
        if across in range(self.cells_across) and up in range(self.cells_up+1):
            return self.ns_walls[across][up]
        return None

    def _ew_wall(self, across, up):
        if across in range(0, self.cells_across+1) and up in range(0, self.cells_up):
            return self.ew_walls[across][up]
        return None

    def cell(self, across, up):
        if across in range(0, self.cells_across) and up in range(0, self.cells_up):
            return self.cells[across][up]
        return None

    def tk_paint(self):
        for i in range(len(self.ns_walls)):
            for j in range(len(self.ns_walls[i])):
                self.ns_walls[i][j].tk_paint()
        for i in range(len(self.ew_walls)):
            for j in range(len(self.ew_walls[i])):
                self.ew_walls[i][j].tk_paint()
        # for i in range(len(self.cells)):
        #     for j in range(len(self.cells[i])):
        #         self.floors[i][j].tk_paint(self.cells[i][j])

    def string(self):  # __str__ method here is just for easy visualisation purposes.
        line = "Level %s\n" % (1 + self.level)
        for j in range(self.cells_up+1):  # reversed: print goes from top to bottom..
            line_ns = ""
            line_ew = ""
            for i in range(self.cells_across+1):
                line_ns += str(self.corners[i][j])
                if self._ns_wall(i, j):
                    line_ns += str(self._ns_wall(i, j))
                if self._ew_wall(i, j):
                    line_ew += str(self._ew_wall(i, j))
                if self.cell(i, j):
                    line_ew += str(self.cell(i, j))
            line += line_ns + "\n" + line_ew + "\n"
        return line
