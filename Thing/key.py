from tkinter import HIDDEN
from Thing.item import Item
from Maze.cell import Cell

# So a key can be picked up, dropped off, or exchanged.
# But this isn't a key in that sense!  It's a key generator.

class Key(Item):

    identity = 0

    def __init__(self, gate_cell):
        super().__init__()
        self.name = self.get_identity()
        self.gate_cell = gate_cell
        self.requires_exchange = False
        self.exchange = set()    # set of key(s) to exchange

    def offset(self):
        return 4

    def select(self, keychain):
        if self.requires_exchange:
            if not self.exchange.isdisjoint(keychain):
                new_chain = self.exchange.difference(keychain)
                keychain.clear()
                keychain.copy(new_chain)
                keychain.add(self.name)
        else:
            keychain.add(self.name)

    def shape(self, canvas):
        fill_colour = "yellow" if self.requires_exchange else "white"
        return [
            canvas.create_rectangle(self.offset(), self.offset(), self.size // 2, self.size // 2, width=2, outline="green", fill=fill_colour),
            canvas.create_text(self.size // 4, self.size // 4, font=("Monaco", self.size // 3), width=1, text=self.name)
        ]

    @staticmethod
    def get_identity():
        keys = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789abcdefghijklmnopqrstuvwxyz"
        key = keys[Key.identity % (len(keys) + 1)]
        Key.identity += 1
        return key


