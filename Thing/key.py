from tkinter import HIDDEN
from Thing.movable import Movable
from Maze.cell import Cell


class Key(Movable):

    def __init__(self):
        super().__init__()

    def shape(self, canvas):
        return [
            canvas.create_rectangle(self.offset, self.offset, self.size, self.size, width=2, outline="green", fill="white", state=HIDDEN),
            canvas.create_text(Cell.size // 2, Cell.size // 2, font=("Monaco", Cell.size // 2), width=1, text="A")
        ]


