# encoding: utf-8
from Maze.util import Com
import random


class Cell:
    size = 20
    last = None
    last_mined = None

    def __init__(self, dim, wns, wew, level):
        self.key  = None  # No key on initialisation.
        self.gate = None  # No rune on initialisation.
        self.rune = None  # No rune on initialisation.
        self.dim = dim
        self.exit_count = 0

        self.level = level
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

    def name(self):
        return str(self.dim)

    def calc_values(self):
        pass
        # self.exit_count = len(self.exits())

    def move(self, com, key_list):
        if com in self.floors and self.floors[com] and not self.floors[com].solid:
            return self.floors[com].cells[com.opposite]
        if com in self.walls and self.walls[com]:
            wall = self.walls[com]
            if not wall.is_wall():
                next_cell = wall.cells[com]
                if next_cell.gate:
                    return self if next_cell.gate.unlocked_with not in key_list else next_cell
                if next_cell.key:
                    next_cell.key.select(key_list)
                    # key_list.add(next_cell.key.name)
                return next_cell
        return self

    def neighbours(self):
        return [self.floors[c].cells[c] for c in self.floor_exits()] + \
               [self.walls[c].cells[c] for c in self.level_exits()]

    def exits(self):
        return self.level_exits() + self.floor_exits()

    def floor_exits(self):
        return [k for k, v in self.floors.items() if v and not v.solid]

    def level_exits(self):
        return [k for k, v in self.walls.items() if v and not v.is_wall()]

    def count_level_exits(self):
        count = 0
        for wall in list(self.walls.values()):
            if not wall.is_wall():
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
            if not self.floors[com.opposite] or self.floors[com.opposite].solid:
                cell = self.floors[com].cells[com.opposite]
                if cell and cell.good_for_stairs():
                    walls.append(com)
        return walls

    def stairs(self):
        if self.floors[Com.F] and not self.floors[Com.F].solid:
            return self.floors[Com.F].cells[Com.C]
        if self.floors[Com.C] and not self.floors[Com.C].solid:
            return self.floors[Com.C].cells[Com.F]
        return []

    def good_for_stairs(self):
        """
        :return: boolean representing if this cell is good for stairs to be built to.
        """
        # if self.floor
        return not self.mined and not self.stairs() and len(self.level_walls_to_be_dug([])) > 0

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
                cf = random.choice([Com.C, Com.F])
                walls = self.stairs_to_be_dug(cf, walls)
                if not walls:  #
                    walls = self.stairs_to_be_dug(cf.opposite, walls)
        return walls

    def is_a_passage(self):
        exits = self.walls_that_can_be_dug()
        if not exits:
            exits = self.stairs()
            if not exits:
                exits = self.level_exits()
                return len(exits) == 2 and exits[0] == exits[1].opposite
        return False

    # make_door_in is done on self's side.
    def make_door_in(self, com, kind=None):
        if com == Com.C or com == Com.F:
            cell = self.floors[com].make_hole(com)
            if cell:
                Cell.last = com
                cell.stairs_coming_in(com.opposite)
        else:
            cell = self.walls[com].make_door(com, kind)
        if cell:
            Cell.last_mined = cell
        return cell

    def stairs_coming_in(self, com):
        self.mined = True
        walls = self.level_exits()
        random.shuffle(walls)
        while walls and len(walls) > 1:
            wall = walls.pop()
            wall.blocked = True

    def change_rune(self, the_rune=None):  # Accepts a rune if one is passed.
        result = self.rune
        self.rune = the_rune
        return result

    def __str__(self):
        if self.rune:
            return self.rune
        if self.floors[Com.F] and not self.floors[Com.F].solid:
            return '⍌'
        if self.floors[Com.C] and not self.floors[Com.C].solid:
            return '⍓'
        return " "

    def __cmp__(self, other):
        return self.dim == other.dim
