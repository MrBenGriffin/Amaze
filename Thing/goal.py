from Thing.item import Item

class Goal(Item):

    def __init__(self, cell):
        super().__init__()
        self.cell = cell

    def offset(self):
        return 4

    def shape(self, canvas):
        fill_colour = "green"
        return [
            canvas.create_rectangle(self.offset(), self.offset(), self.size // 2, self.size // 2, width=2, outline="yellow", fill=fill_colour),
        ]
