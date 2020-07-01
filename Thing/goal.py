from Thing.item import Item

class Goal(Item):

    def __init__(self, cell):
        super().__init__()
        self.cell = cell

    def tk_init(self, maze, cell, size=0.75):
        super().tk_init(maze, cell, size)

    def shape(self, canvas):
        fill_colour = "green"
        return [
            canvas.create_rectangle(0, 0, self.size, self.size, width=2, outline="yellow", fill=fill_colour)
        ]
