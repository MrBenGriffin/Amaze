from tkinter import *
from Maze.maze import Maze
from Maze.cell import Cell
from Bod.miner import Miner

maze_width = 120
maze_height = 70
cell_size = Cell.hi

root = Tk()

canvas = Canvas(root, width=cell_size * (maze_width + 2), height=cell_size * (maze_height + 2), bg='gray')
canvas.grid(columns=1, rows=1)

the_maze = Maze(maze_width, maze_height)
the_miner = Miner()
sys.setrecursionlimit(10000)
the_miner.dig(the_maze.cell(0, 0))
# Okay, so building 120x70 rooms takes the miner a few seconds. We aren't going to use this miner
# anyhow, as he always makes boringly long twisty corridors.

# Paint the maze itself. we will need to update rune doors at some point.
# Either we should paint them as open/closed and then overlay, or just redraw everything.
# Needless to say, it's also faster to paint using the walls, not the cells...
[[the_maze.cell(i, j).tk_paint(canvas) for i in range(maze_width)] for j in range(maze_height)]

root.mainloop()
