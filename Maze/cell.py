# encoding: utf-8
from Maze.cross import Cross
from Maze.util import Com
import random


class Cell:
    size = 20
    last = None

    def __init__(self, dim, wns, wew):
        self.rune = None  # No rune on initialisation.
        self.tk_id = None
        self.dim = dim
        self.mined = False
        self.floors = {Com.C: None, Com.F: None}
        self.walls = {Com.N: wns[dim.x][dim.y + 1],
                      Com.E: wew[dim.x + 1][dim.y],
                      Com.S: wns[dim.x][dim.y],
                      Com.W: wew[dim.x][dim.y]
                      }
        self.walls[Com.N].set_cell(self, Com.S)
        self.walls[Com.E].set_cell(self, Com.W)
        self.walls[Com.S].set_cell(self, Com.N)
        self.walls[Com.W].set_cell(self, Com.E)

        # for com in self.walls.keys():
        #     self.walls[com].set_cell(self, com.opposite)

    def name(self) -> str:
        return str(self.dim)

    def exits(self):
        dict_of_exits = self.level_exits()
        for compass, floor in self.floors.items():
            if not floor["solid"]:
                dict_of_exits[compass] = compass
        return dict_of_exits

    def level_exits(self):
        dict_of_exits = {}
        for compass, wall in self.walls.items():
            if not wall.is_solid():
                dict_of_exits[compass] = compass
        return dict_of_exits

    def count_level_exits(self):
        count = 0
        for wall in list(self.walls.values()):
            if not wall.is_solid():
                count += 1
        return count

    def level_walls_to_be_dug(self, walls):
        for compass, wall in self.walls.items():
            if wall.can_be_dug(compass):
                walls.append(compass)
        return walls

    def stairs_to_be_dug(self, com, walls):
        """
            See if this is a good point for stairs.
            * This cell must be a dead-end.
            * Next floor must be 'good_for_stairs'
            :return: list[Com] of available stairs.
        """
        if self.floors[com]:
            cell = self.floors[com].other(com)
            if cell and cell.good_for_stairs():
                walls.append(com)
        return walls

    def is_stairs(self):
        """
        :return: boolean indicating if there are stairs in this cell.
        """
        return (not self.floors[Com.C] and not self.floors[Com.C].solid) \
            or not self.floors[Com.F].solid

    def good_for_stairs(self):
        """
        :return: boolean representing if this cell is good for stairs to be built to.
        """
        return not self.mined and len(self.level_walls_to_be_dug([])) > 0

    def walls_that_can_be_dug(self):
        """
        :return: list [Com] that may be dug..
        """
        # First of all check to see if there are walls on this level.
        # We don't want to go up or down if we can mosey along.
        walls = self.level_walls_to_be_dug([])
        if not walls and self.count_level_exits() == 1:
            if not walls and Cell.last:  #
                walls = self.stairs_to_be_dug(Cell.last, walls)
            if not walls:  #
                walls = self.stairs_to_be_dug(Com.C, walls)
                walls = self.stairs_to_be_dug(Com.F, walls)
        return walls

    # make_door_in is done on self's side.
    def make_door_in(self, com, kind=None):
        if com == Com.C or com == Com.F:
            cell = self.floors[com].make_hole(com)
            if cell:
                Cell.last = com
                self.floors[com].tk_paint(com)
                cell.stairs_coming_in(com.opposite)
            return cell
        else:
            return self.walls[com].make_door(com, kind)

    def stairs_coming_in(self, com):
        self.floors[com].tk_paint(com)
        walls = self.level_exits()
        random.shuffle(walls)
        while walls and len(walls) > 1:
            wall = walls.pop()
            wall.blocked = True

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
