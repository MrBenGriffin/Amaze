from tkinter import *
from Maze.maze import Maze
from Maze.cell import Cell
from Bod.miner import Miner
maze_width = 0
while True:
    try:
        maze_width =  int(input('Maze Width?: '))
    except ValueError:
        print("That's not a number!")
        continue
    else:
        print('thanks')
        break
maze_height = 0
while True:
    try:
        maze_height = int(input('Maze Height?: '))
    except ValueError:
        print("That's not a number!")
        continue
    else:
        print('thanks')
        break

cell_size = Cell.size

root = Tk()
if maze_width > 0 and maze_height > 0:
    canvas = Canvas(root, width=cell_size * (maze_width + 2), height=cell_size * (maze_height + 2),
                bg='gray')
    canvas.grid(columns=1, rows=1)

    the_maze = Maze(maze_width, maze_height)
    the_miner = Miner()
    sys.setrecursionlimit(10000)
    the_miner.dig(the_maze.cell(0, 0))
    # Okay, so building 120x70 rooms takes the miner a few seconds. We aren't going to use this miner
    # Paint the maze itself. we will need to update rune doors at some point.
    # Either we should paint them as open/closed and then overlay, or just redraw everything.
    the_maze.tk_paint(canvas)
    root.mainloop()
else:
    print('You need to set a width and a height')
