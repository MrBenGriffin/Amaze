from tkinter import *
from Maze.maze import Maze
from Maze.cell import Cell
from Bod.miner import Miner
cell_size = Cell.size

#Initialise a window
root = Tk()

"""Function to check what is being typed into entry is an intiger
 - We are checking letter by letter"""
def testVal(inStr,i,acttyp):
    #i is the index of the char string
    #acttyp is the type of action
    #inStr is the value
    ind=int(i)
    if acttyp == '1': #if the action is an insert
        if not inStr[ind].isdigit(): #if the character is not a digit
            return False #don't let it go in
    return True

#register the above function so it can be called from an Entry
intChecker = root.register(testVal)

#This function pulls the sizes as defined by the Entry boxes and calls the maze
def getSize():
    maze_width = int(E1.get())  # grab the entry of textbox 1 as an integer
    maze_height = int(E2.get())  # grab the entry of textbox 2 as an integer

    # kill the window as it currently stands
    root.destroy()

    # make the maze
    createMaze(maze_width, maze_height)

# Create the textboxes for width and height
"""valid percent substitutions for validatecommand (from the Tk entry man page)
# %d = Type of action (1=insert, 0=delete, -1 for others)
# %i = index of char string to be inserted/deleted, or -1
# %P = value of the entry if the edit is allowed
# %s = value of entry prior to editing
# %S = the text string being inserted or deleted, if any
# %v = the type of validation that is currently set
# %V = the type of validation that triggered the callback
#      (key, focusin, focusout, forced)
# %W = the tk name of the widget"""

label1 = Label( root, text="Maze Width")
E1 = Entry(root, bd=3, validate="key", validatecommand=(intChecker, '%P','%i','%d')) #validate=key means it checks each letter as typed
label2 = Label( root, text="Maze Height")
E2 = Entry(root, bd=3, validate="key", validatecommand=(intChecker, '%P','%i','%d'))

#Create the submit button to call the getSize function
submit = Button(root, text ="Submit", command = getSize)

#Add all of the text boxes and stuff to the grid
label1.grid()
E1.grid()
label2.grid()
E2.grid()
submit.grid()

#Actually create the maze
def createMaze(w, h):
    root = Tk()
    #First check we are not making it with no size
    if w > 0 and h > 0:
        canvas = Canvas(root, width=cell_size * (w + 2), height=cell_size * (h + 2),
                    bg='gray')
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

root.mainloop()