from Maze.cell import Dim
import random


class Miner:
    """
    Miner is  a simple solitary random walk algorithm.
    The miner starts at a cell in the mine, then chooses a wall to knock down.
    Mining Rule #1 is that he cannot knock down a wall into a pre-visited cell.
    When he gets to a dead end (all the surrounding cells are visited or are edges) then
    he backtracks to the previous cell he visited.

    So.
        (1) Get a dict of walls that I can dig from my current cell.
        (2) If the dict isn't empty, shuffle the list (actually just the keys).
        (3) ... and then for each, check it still can be dug (because we are recursive).
        (4)     ... and it it can be dug, dig it and move there, marking where I've come from, and go to (1)
        (6) continue the good work from my previous cell..

    """

    def dig(self, cell):
        walls_to_dig = cell.digs()
        if len(walls_to_dig) > 0:
            walls_list = list(walls_to_dig)
            random.shuffle(walls_list)
            for wall in walls_list:
                if walls_to_dig[wall].can_be_dug():
                    next_cell = cell.make_door(wall)
                    self.dig(next_cell)

