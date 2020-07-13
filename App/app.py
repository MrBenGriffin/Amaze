from random import choice
from tkinter import *

from Bod.gatemaker import Gatemaker
from Bod.inchworm import Inchworm
from Maze.maze import Maze
from Bod.miner import Miner
from Bod.lister import Lister
from Bod.slaver import Slaver
from Bod.gamer import Gamer
from Bod.robot import Robot
from App.config import Config
from Thing.goal import Goal
from Thing.start import Start


class App(object):
    def __init__(self, tk_root):
        self.miner = None
        self.gamer = None
        self.robot = None
        self.start_cell = None
        self.goal_cell = None
        self.root = tk_root
        self.maze_windows = []
        self.config = Config(self.root, self.create_maze)

# width, height, levels, cell_size, digger, show_dig
    def create_maze(self, cells_across, cells_up, levels, cell_size, digger, show_dig):
        x = self.root.winfo_x()
        y = self.root.winfo_y()

        maze_window = Toplevel(self.root)
        maze_window.geometry("+%d+%d" % (x, y + 200))
        self.maze_windows.append(maze_window)

        bods_window = Toplevel(self.root)
        bods_window.geometry("+%d+%d" % (x+300, y))
        self.maze_windows.append(bods_window)

        the_maze = Maze(cells_across, cells_up, levels, cell_size)
        the_maze.tk_init_maze(maze_window)

        if digger == 1:
            self.miner = Miner(the_maze)
        elif digger == 2:
            self.miner = Lister(the_maze)
        else:
            self.miner = Slaver(the_maze)

        self.miner.dig(the_maze.at(Maze.start))
        the_maze.add_bod(self.miner)
        the_maze.mine(self.miner, show_dig)
        the_maze.remove_bod(self.miner)

        # Choose start and goal.
        self.start_cell = the_maze.cell(0, 0, 0)

        worm = Inchworm(the_maze)
        cell_distances = worm.distances(self.start_cell)
        furthest = len(cell_distances) - 1    # first is zero, and others go up from there...
        far_cells = cell_distances[furthest]  # list of furthest cells

        # Make start and goal
        the_maze.add_thing(self.start_cell, Start(the_maze))
        self.goal_cell = the_maze.at(choice(far_cells))
        the_maze.add_thing(self.goal_cell, Goal(the_maze))

        # Make gates and decoy gates
        # gate_maker = Gatemaker(the_maze, worm)
        # gate_maker.make(start_cell, self.goal_cell)

        # Make robot
        # self.robot = Robot(the_maze)
        # self.robot.go(the_maze.at(Maze.start))
        # self.robot.goal = self.b
        # the_maze.add_bod(self.robot)

        # Make Gamer
        # self.gamer = Gamer(the_maze)
        # self.gamer.go(the_maze.at(Maze.start))
        # self.gamer.goal = self.goal_cell
        # the_maze.add_bod(self.gamer)

        the_maze.tk_init_things()
        the_maze.tk_init_bods(bods_window)
        the_maze.tk_paint()


    @staticmethod
    def run():
        the_root = Tk()
        App(the_root)
        the_root.mainloop()


if __name__ == "__main__":
    App.run()
