# from tkinter import HIDDEN
from Thing.item import Item
# from Maze.cell import Cell

# So a key can be picked up, dropped off, or exchanged.
# But this isn't a key in that sense!  It's a key generator.
# Maybe we should allow two-way key exchange A<-->B
# it would be easier (no need for rev. key)

class Key(Item):

    identity = 0

    def __init__(self, gate_cell, key_to_exchange=None, key_name=None):
        super().__init__()
        self.name = key_name if key_name else self.get_identity()
        self.exch = key_to_exchange
        self.gate_cell = gate_cell
        self.requires_exchange = key_to_exchange is not None
        self.exchange = {self.exch} if self.exch else {}

    def tk_init(self, size=0.5):
        super().tk_init(size)

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
        if self.requires_exchange:
            exch = '*'
            text_scale = int(self.size * 0.5)
            text_offset = self.size - self.size * 0.8 * 0.66
            text_delta = int(self.size * 0.2)
            return [
                canvas.create_rectangle(0, 0, self.size, self.size, width=2, outline="green", fill=fill_colour),
                canvas.create_text(text_offset+text_delta, text_offset+text_delta, font=("Helvetica", text_scale), text=self.name),
                canvas.create_text(text_offset-text_delta, text_offset-text_delta, font=("Helvetica", text_scale), text=self.exch)
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

