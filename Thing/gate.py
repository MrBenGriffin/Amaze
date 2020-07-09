from random import choice
from Thing.item import Item
# from Bod.keymaker import Keymaker
# from Maze.maze import Maze

# We need to add Gates - these can go on cells where there is an entrance/exit.
# Gates don't -need- to be directional if we use key exchanges, because one can only go forward with the correct key
# ... a ... A ...a->b ... B ... b->c ... C ...c->a A, etc.

class Gate(Item):

    def __init__(self, key=None, bi_directional=True):
        super().__init__()
        self.unlocked_with = key.name if key else None
        self.bi_directional = bi_directional

    def tk_init(self, size=0.8):
        super().tk_init(size)

    def shape(self, canvas):
        outline_colour = "white" if self.bi_directional else "red"
        text_scale = int(self.size * 0.8)
        text_offset = self.size - text_scale * 0.66
        return [
            canvas.create_rectangle(0, 0, self.size, self.size, width=int(self.size * 0.1), fill="green", outline=outline_colour),
            canvas.create_text(text_offset, text_offset, font=("Monaco", text_scale), width=1, text=self.unlocked_with)
        ]
