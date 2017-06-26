from Maze.cell import Dim
import random


class Miner:
    def __init__(self, maze, x, y):
        self.x = x
        self.y = y
        self.maze = maze    # Each cell has a property 'mined' which is whether or not the miner has visited.
        self.maze.set_mined(self.x, self.y, Dim(None, None))

    def dig(self):
        digs = self.maze.digs(self.x, self.y)
        if len(digs) != 0:
            dirs = list(digs)
            random.shuffle(dirs)
            for dig in dirs:
                if digs[dig].can_be_dug():
                    cell = self.maze.make_door(self.x, self.y, dig)
                    was = Dim(self.x, self.y)
                    self.x = cell.dim.x
                    self.y = cell.dim.y
                    self.maze.set_mined(self.x, self.y, was)
                    self.dig()
        prev = self.maze.get_mined(self.x, self.y)
        self.x = prev.x
        self.y = prev.y
