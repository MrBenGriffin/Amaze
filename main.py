from Maze.maze import Maze
from Bod.miner import Miner


def maze():

    the_maze = Maze(40, 40)
    the_miner = Miner(the_maze, 0, 0)
    the_miner.dig()
    print(the_maze)


if __name__ == "__main__":
    maze()  #

