# encoding: utf-8
from enum import Enum
from Maze.cross import Cross
import random

class Com(Enum):
    N = 'N'  # North
    S = 'S'  # South
    E = 'E'  # East
    W = 'W'  # West
    C = 'C'  # Ceiling
    F = 'F'  # Floor


class Cell:
    size = 20
    last = None

    def __init__(self, dim, wns, wew):
        self.rune = None  # No rune on initialisation.
        self.tk_id = None
        self.canvas = None
        self.dim = dim
        self.mined = False
        self.walls = {Com.N: wns[dim.x][dim.y + 1],
                      Com.E: wew[dim.x + 1][dim.y],
                      Com.S: wns[dim.x][dim.y],
                      Com.W: wew[dim.x][dim.y]
                      }
        self.walls[Com.N].set_cell(self, Com.S)
        self.walls[Com.E].set_cell(self, Com.W)
        self.walls[Com.S].set_cell(self, Com.N)
        self.walls[Com.W].set_cell(self, Com.E)
        self.floors = {
            Com.C: {'cell': None, 'solid': True},
            Com.F: {'cell': None, 'solid': True}
        }

    def set_floor(self, up, down):
        if up:
            self.floors[Com.C] = {'cell': up.cell(self.dim.x, self.dim.y), 'solid': True}
        if down:
            self.floors[Com.F] = {'cell': down.cell(self.dim.x, self.dim.y), 'solid': True}

    def name(self) -> str:
        return str(self.dim)

    def exits(self):
        dict_of_exits = self.level_exits(self)
        for compass, floor in self.floors.items():
            if not floor["solid"]:
                dict_of_exits[compass] = floor["cell"]
        return dict_of_exits

    def level_exits(self):
        dict_of_exits = {}
        for compass, wall in self.walls.items():
            if not wall.is_solid():
                dict_of_exits[compass] = wall.other(self)
        return dict_of_exits

    def level_walls_to_be_dug(self, walls):
        """
            Walls that may be dug at this level.
            We don't really want stairs to have more than one
            exit / entrance, but it's tricky..
        """
        for compass, wall in self.walls.items():
            if wall.can_be_dug():
                walls.append(compass)
        return walls

    def stairs_to_be_dug(self, com, walls):
        """
            See if this may be dug.
        """
        cell = self.floors[com]["cell"]
        if cell and cell.good_for_stairs():
            walls.append(com)
        return walls

    def is_stairs(self):
        return not self.floors[Com.C]["solid"] or not self.floors[Com.F]["solid"]

    def good_for_stairs(self):
        return not self.mined and len(self.level_walls_to_be_dug([])) == 4

    def walls_that_can_be_dug(self):
        walls = self.level_walls_to_be_dug([])
        exit_count = len(self.level_exits())
        if not walls and Cell.last and exit_count == 1:  #
            walls = self.stairs_to_be_dug(Cell.last, walls)
        if not walls and exit_count == 1:  #
            walls = self.stairs_to_be_dug(Com.C, walls)
            walls = self.stairs_to_be_dug(Com.F, walls)
        return walls

    def tk_paint(self, canvas):
        if not self.canvas:
            self.canvas = canvas
        c = self.walls[Com.N].solid
        f = self.walls[Com.S].solid
        x0 = f[0] + 4
        x1 = f[2] - 4
        y0 = c[1] - 4
        y1 = f[1] + 4
        if not self.floors[Com.C]["solid"]:
            self.tk_id = canvas.create_line((x0, y0, x1, y0, x1, y1, x0, y0), width=2, fill='red')
        elif not self.floors[Com.F]["solid"]:
            self.tk_id = canvas.create_line((x0, y0, x0, y1, x1, y0, x0, y0), width=2, fill='blue')

    def make_door_in(self, com, kind=None):
        self.mined = True
        if com == Com.C or com == Com.F:
            floor = self.floors[com]
            cell = floor["cell"]
            floor["solid"] = False
            if self.canvas:
                self.tk_paint(self.canvas)
            if com == Com.C:
                Cell.last = Com.C
                return cell.start(Com.F)
            else:
                Cell.last = Com.F
                return cell.start(Com.C)
        else:
            return self.walls[com].make_door(self, kind)

    def start(self, com):
        self.mined = True
        self.floors[com]["solid"] = False
        walls = self.level_exits()
        random.shuffle(walls)
        while len(walls) > 1:
            wall = walls.pop()
            wall.blocked = True
        if self.canvas:
            self.tk_paint(self.canvas)
        return self

    def change_rune(self, the_rune=None):  # Accepts a rune if one is passed.
        result = self.rune
        self.rune = the_rune
        return result

    def str_nwn(self):

        right = bottom = left = top = False
        north_wall = self.walls[Com.N]
        west_wall = self.walls[Com.W]

        if north_wall:
            n_cell = north_wall.other(self)
            right = north_wall.is_solid()
            if n_cell and n_cell.walls[Com.W]:
                top = n_cell.walls[Com.W].is_solid()
        if west_wall:
            w_cell = west_wall.other(self)
            bottom = west_wall.is_solid()
            if w_cell and w_cell.walls[Com.N]:
                left = w_cell.walls[Com.N].is_solid()

        nw = Cross(top, left, bottom, right)
        if right:
            n = Cross.XLXR
        else:
            n = " "
        return nw.cross + n

    def str_sws(self):
        left = bottom = False
        right = self.walls[Com.S].is_solid()
        top = self.walls[Com.W].is_solid()
        w_cell = self.walls[Com.W].other(self)
        if w_cell:
            left = True
        return Cross(top, left, bottom, right).cross + Cross.XLXR

    def str_ne(self):
        return Cross(self.walls[Com.N].other(self) is not None,
                     self.walls[Com.N].is_solid(),
                     True,
                     False).cross

    def __cmp__(self, other):
        return self.dim == other.dim
