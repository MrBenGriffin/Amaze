from tkinter import *
from Maze.maze import Maze
from Bod.miner import Miner
from Bod.lister import Lister
from Bod.slaver import Slaver
from Bod.gamer import Gamer, Goal
from Bod.robot import Robot
from App.config import Config


class App(object):
    def __init__(self, tk_root):
        self.miner = None
        self.gamer = None
        self.robot = None
        self.goal = None
        self.root = tk_root
        self.maze_windows = []
        self.config_window = tk_root     # for the moment, we shall use root for config.
        self.config = Config(self.config_window, self.create_maze)

# width, height, levels, cell_size, digger, show_dig
    def create_maze(self, cells_across, cells_up, levels, cell_size, digger, show_dig):
        maze_window = Toplevel(self.root)
        the_maze = Maze(cells_across, cells_up, levels, cell_size)
        the_maze.tk_init(maze_window)
        if digger == 1:
            self.miner = Miner(the_maze)
        elif digger == 2:
            self.miner = Lister(the_maze)
        else:
            self.miner = Slaver(the_maze)
        self.miner.dig(the_maze.at(Maze.start))
        self.goal = Goal(the_maze)
        self.gamer = Gamer(the_maze)
        self.robot = Robot(the_maze)

        self.gamer.go(the_maze.at(Maze.start))
        self.robot.go(the_maze.at(Maze.start))
        self.goal.go(the_maze.cell(cells_across - 1, cells_up - 1, levels - 1))
        self.gamer.goal = self.goal
        self.robot.goal = self.goal

        the_maze.add_bod(self.miner, show_dig)
        the_maze.add_bod(self.gamer, True)
        the_maze.add_bod(self.robot, True)
        the_maze.add_bod(self.goal, True)
        the_maze.tk_paint()
        self.maze_windows.append(maze_window)

    @staticmethod
    def run():
        the_root = Tk()
        App(the_root)
        the_root.mainloop()

if __name__ == "__main__":
    App.run()
