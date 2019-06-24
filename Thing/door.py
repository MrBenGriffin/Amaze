from tkinter import HIDDEN
from Thing.item import Item
from Bod.keymaker import Keymaker
from Maze.maze import Maze


class Door(Item):

    def __init__(self):
        super().__init__()

    # Need to add labels onto this soon.
    @staticmethod
    def make(maze, cell):
        key_maker = Keymaker(maze)
        key_maker.go(maze.at(Maze.start))
        key_maker.goal = cell
        while not key_maker.finished():
            key_maker.run()
        if key_maker.set_key():
            maze.add_thing(cell, Door())

    def tk_init(self, maze, cell):
        super().tk_init(maze, cell)

    def shape(self, canvas):
        return [canvas.create_rectangle(self.offset, self.offset, self.size, self.size, width=2, fill="green", state=HIDDEN)]

