from tkinter import HIDDEN, NORMAL
from Maze.cell import Cell


class Item(object):

    # All Items are found in a cell (if they aren't in one, they are invisible).
    # Sometimes they inherit the cell that they are in from their owner...
    # Everything else about them is just for calculating the drawing of them...
    def __init__(self):
        self.cell = None
        self.maze = None
        self.ids = []
        self.canvases = []
        self.levels = 1
        self.body = None
        self.size = Cell.size - Cell.size // 4
        self.offset = Cell.size // 4
        self.active = True

    # Default method.
    def shape(self, canvas):
        return [canvas.create_rectangle(self.offset, self.offset, self.size, self.size, outline="white", fill="red", state=HIDDEN)]

    def tk_init(self, maze, cell):
        self.maze = maze
        self.cell = cell
        self.levels = len(maze.levels)
        for level in maze.levels:
            self.canvases.append(level.tk_level)
            canvas = level.tk_level
            shape = self.shape(canvas)
            self.ids.append(shape)
        self.tk_move()

    def tk_move(self):
        x = self.cell.dim.x * Cell.size + self.offset
        y = self.cell.dim.y * Cell.size + self.offset
        canvas = self.canvases[self.cell.dim.z]
        items = self.ids[self.cell.dim.z]
        for item in items:
            values = canvas.coords(item)
            if len(values) == 4:
                canvas.coords(item, values[0]+x, values[1]+y, values[2]+x, values[3]+y)
            else:
                canvas.coords(item, values[0]+x, values[1]+y)

    def tk_paint(self):
        if self.active:
            for z in range(self.levels):
                if self.cell.dim and z == self.cell.dim.z:
                    for item in self.ids[z]:
                        self.canvases[z].itemconfig(item, state=NORMAL)
                else:
                    for item in self.ids[z]:
                        self.canvases[z].itemconfig(item, state=HIDDEN)
