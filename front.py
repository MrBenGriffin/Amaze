from tkinter import *
from Maze.maze import Maze
from Maze.cell import Cell
from Bod.miner import Miner
cell_size = Cell.size

# Initialise a window
entry = Tk()
frame = Frame(entry)
frame.grid(columns=2, rows=3)


# This function pulls the sizes as defined by the Entry boxes and calls the maze
def get_size():
    maze_width = int('0'+maze_width_entry.get())  # grab the entry of textbox 1 as an integer
    maze_height = int('0'+maze_height_entry.get())  # grab the entry of textbox 2 as an integer
    if maze_height and maze_width:
        create_maze(maze_width, maze_height)

# Create the text-boxes for width and height
"""valid percent substitutions for validate command (from the Tk entry man page)
# %d = Type of action (1=insert, 0=delete, -1 for others)
# %i = index of char string to be inserted/deleted, or -1
# %P = value of the entry if the edit is allowed
"""

# This is a simple input validation that accepts numbers between 1 and 250.
int_checker = frame.register(lambda text, i, action: action != '1' or text[int(i)].isdigit() and 0 < int(text) < 250)

maze_width_label = Label(frame, text="Maze Width")    # validate=key means it checks each letter as typed
maze_width_entry = Entry(frame, bd=3, validate="key", validatecommand=(int_checker, '%P', '%i', '%d'))
maze_height_label = Label(frame, text="Maze Height")
maze_height_entry = Entry(frame, bd=3, validate="key", validatecommand=(int_checker, '%P', '%i', '%d'))

# Create the submit button to call the getSize function
submit = Button(frame, text="Submit", command=get_size)

# Add all of the text boxes and stuff to the grid
maze_width_label.grid(row=0, column=0, sticky=E)
maze_width_entry.grid(row=0, column=1)
maze_height_label.grid(row=1, column=0, sticky=E)
maze_height_entry.grid(row=1, column=1)
submit.grid(row=2, columnspan=2)


# Actually create the maze
def create_maze(w, h):
    root = Tk()
    # First check we are not making it with no size
    if w > 0 and h > 0:
        canvas = Canvas(root, width=cell_size * (w + 2), height=cell_size * (h + 2), bg='gray')
        canvas.grid(columns=1, rows=1)

        the_maze = Maze(w, h)
        the_miner = Miner()
        sys.setrecursionlimit(10000)
        the_miner.dig(the_maze.cell(0, 0))
        """Okay, so building 120x70 rooms takes the miner a few seconds. We aren't going to use this miner
        Paint the maze itself. we will need to update rune doors at some point.
        Either we should paint them as open/closed and then overlay, or just redraw everything."""
        the_maze.tk_paint(canvas)

    else:
        print('We somehow got here with no width and height')

entry.mainloop()
