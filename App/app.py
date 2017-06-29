from tkinter import *
from Maze.maze import Maze
from Bod.miner import Miner
from App.config import Config


class App(object):
    def __init__(self, tk_root):
        self.root = root
        self.maze_windows = []
        self.config_window = tk_root     # for the moment, we shall use root for config.
        self.config = Config(self.config_window, self.create_maze)

    def create_maze(self, cells_across, cells_up, cell_size):
        maze_window = Toplevel(self.root)
        the_maze = Maze(cells_across, cells_up, cell_size)
        the_maze.tk_init(maze_window)
        the_miner = Miner()
        the_maze.add_bod(the_miner)
        the_miner.dig(the_maze.cell(0, 0))
        the_maze.tk_paint()
        self.maze_windows.append(maze_window)

if __name__ == "__main__":
    sys.setrecursionlimit(10000)
    root = Tk()
    app = App(root)
    root.mainloop()
