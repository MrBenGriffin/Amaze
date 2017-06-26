from Maze.maze import Maze
from Bod.miner import Miner


def maze():

    the_maze = Maze(60, 20)
    the_miner = Miner()
    the_miner.dig(the_maze.cell(0, 0))
    print(the_maze)


if __name__ == "__main__":
    maze()  #

