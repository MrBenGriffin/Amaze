from tkinter import *
from Maze.maze import Maze
from Bod.miner import Miner
from Bod.lister import Lister
from Bod.slaver import Slaver
from App.config import Config


class App(object):
    def __init__(self, tk_root):
        self.root = tk_root
        self.maze_windows = []
        self.config_window = tk_root     # for the moment, we shall use root for config.
        self.config = Config(self.config_window, self.create_maze)

    def create_maze(self, cells_across, cells_up, cell_size, digger):
        maze_window = Toplevel(self.root)
        the_maze = Maze(cells_across, cells_up, cell_size)
        the_maze.tk_init(maze_window)
        if digger == 1:
            the_miner = Miner()
        elif digger == 2:
            the_miner = Lister()
        else:
            the_miner = Slaver()
        the_miner.dig(the_maze.cell(0, 0))
        the_maze.add_bod(the_miner)
        the_maze.tk_paint()
        self.maze_windows.append(maze_window)

    @staticmethod
    def run():
        sys.setrecursionlimit(10000)
        the_root = Tk()
        App(the_root)
        the_root.mainloop()


if __name__ == "__main__":
    App.run()
