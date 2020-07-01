from abc import abstractmethod
from tkinter import HIDDEN, NORMAL
from Maze.cell import Cell


class Item(object):

    # All Items are found in a cell (if they aren't in one, they are invisible).
    # Sometimes they inherit the cell that they are in from their owner...
    # Everything else about them is just for calculating the drawing of them...
    def __init__(self):
        self.maze = None
        self.cell = None
        self.canvas = None
        self.body = None
        self.size = None
        self.offset = None
        self.active = True
        self.id = []

    # Default method.
    def shape(self, canvas):
        return [canvas.create_rectangle(0, 0, self.size, self.size, outline="white", fill="red")]

    def tk_init(self, maze, cell, size=0.70):
        self.maze = maze
        self.size = maze.cell_size * size
        self.cell = cell
        self.offset = (maze.cell_size - self.size) // 2
        self.canvas = cell.level.tk_level
        self.id = self.shape(self.canvas)
        self.tk_move()

    def tk_move(self):
        x = self.cell.dim.x * self.cell.size + self.maze.offset + self.offset
        y = self.cell.dim.y * self.cell.size + self.maze.offset + self.offset
        for widget in self.id:
            values = self.canvas.coords(widget)
            if len(values) == 4:
                self.canvas.coords(widget, values[0]+x, values[1]+y, values[2]+x, values[3]+y)
            else:
                self.canvas.coords(widget, values[0]+x, values[1]+y)

    def tk_paint(self):
        pass
