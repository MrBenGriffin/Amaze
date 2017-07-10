from tkinter import *
from Maze.maze import Maze
from Bod.miner import Miner
from Bod.lister import Lister
from Bod.slaver import Slaver
from Bod.gamer import Gamer
from App.config import Config


class App(object):
    def __init__(self, tk_root):
        self.miner = None
        self.gamer = None
        self.root = tk_root
        self.maze_windows = []
        self.config_window = tk_root     # for the moment, we shall use root for config.
        self.config = Config(self.config_window, self.create_maze)

    def create_maze(self, cells_across, cells_up, cell_size, levels, digger, show_dig):
        maze_window = Toplevel(self.root)
        the_maze = Maze(cells_across, cells_up, cell_size, levels)
        the_maze.tk_init(maze_window)
        if digger == 1:
            self.miner = Miner()
        elif digger == 2:
            self.miner = Lister()
        else:
            self.miner = Slaver()
        self.miner.dig(the_maze.cell(0, 0, 0))
        self.gamer = Gamer()
        self.gamer.go(the_maze.cell(0, 0, 0))
        the_maze.add_bod(self.miner, show_dig)
        the_maze.add_bod(self.gamer, True)
        the_maze.tk_paint()
        self.maze_windows.append(maze_window)

    @staticmethod
    def run():
        the_root = Tk()
        App(the_root)
        the_root.mainloop()

if __name__ == "__main__":
    App.run()
