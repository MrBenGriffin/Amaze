from random import choice
from Thing.item import Item
# from Bod.keymaker import Keymaker
# from Maze.maze import Maze

# We need to add Gates - these can go on cells where there is an entrance/exit.
# Doors may be one-directional

class Gate(Item):

    def __init__(self, bi_directional, key):
        super().__init__()
        self.unlocked_with = key.name
        self.bi_directional = bi_directional

    def offset(self):
        return 0

    def tk_init(self, maze, cell):
        super().tk_init(maze, cell)

    def shape(self, canvas):
        outline_colour = "white" if self.bi_directional else "red"
        return [
            canvas.create_rectangle(0, 0, self.size, self.size, width=4, fill="green", outline=outline_colour),
            canvas.create_text(self.size // 2, self.size // 2, font=("Monaco", self.size // 3), width=1, text=self.unlocked_with)
        ]
