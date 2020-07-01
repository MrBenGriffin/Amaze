from tkinter import HIDDEN
from Thing.item import Item
from Maze.cell import Cell

# So a key can be picked up, dropped off, or exchanged.
# But this isn't a key in that sense!  It's a key generator.

class Key(Item):

    identity = 0

    def __init__(self, gate_cell, exchange=(), key_name=None):
        super().__init__()
        self.name = key_name if key_name else self.get_identity()
        self.gate_cell = gate_cell
        self.requires_exchange = len(exchange) != 0
        self.exchange = set(exchange)    # set of key(s) to exchange

    def tk_init(self, maze, cell, size=0.5):
        super().tk_init(maze, cell, size)

    def select(self, keychain):
        if self.requires_exchange:
            if not self.exchange.isdisjoint(keychain):
                for key in self.exchange:
                    keychain.remove(key)
                keychain.add(self.name)
        else:
            keychain.add(self.name)

    def shape(self, canvas):
        fill_colour = "yellow"

        # This shows A/B
        # if self.requires_exchange:
        if True:
            exch = '*'
            if len(self.exchange) == 1:
                for exch in self.exchange:
                    break
            text_scale = int(self.size * 0.5)
            text_offset = self.size - self.size * 0.8 * 0.66
            text_delta = int(self.size * 0.2)
            return [
                canvas.create_rectangle(0, 0, self.size, self.size, width=2, outline="green", fill=fill_colour),
                canvas.create_text(text_offset+text_delta, text_offset+text_delta, font=("Helvetica", text_scale, 'bold'), text=self.name),
                canvas.create_text(text_offset-text_delta, text_offset-text_delta, font=("Helvetica", text_scale), text=exch)
            ]
        else:
            text_scale = int(self.size * 0.8)
            text_offset = self.size - text_scale * 0.66
            return [
                canvas.create_rectangle(0, 0, self.size, self.size, width=2, outline="green", fill=fill_colour),
                canvas.create_text(text_offset, text_offset, font=("Helvetica", text_scale, 'bold'), width=1, text=self.name)
            ]

    @staticmethod
    def get_identity():
        keys = "ABCDEF"
        unused = "GHIJKLMNOPQRSTUVWXYZ0123456789abcdefghijklmnopqrstuvwxyz"
        key = keys[Key.identity % len(keys)]
        Key.identity += 1
        return key

