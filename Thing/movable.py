from tkinter import HIDDEN
from Thing.item import Item


# All Movables are Items.
# They cannot be moved themselves, but will be picked up or dropped off by a Bod.mover.
# At any given time their cell is determined by either being owned or being dropped.

class Movable(Item):

    def __init__(self):
        super().__init__()
        self.owner = None

    def picked(self, taker):
        self.cell = None
        self.owner = taker

    def dropped(self):
        if self.owner:
            self.cell = self.owner.cell()
            self.owner = None

    def shape(self, canvas):
        return [canvas.create_line(0, 0, self.size, self.size, width=5, fill="green", state=HIDDEN)]

    def tk_paint(self):
        if self.owner:
            self.cell = self.owner.cell()
            self.cell = None
        else:
            super().tk_paint()

