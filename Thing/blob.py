from Thing.item import Item

class Blob(Item):

    def __init__(self, colour="yellow", size=0.1):
        self.colour = colour
        self.sized = size
        super().__init__()

    def tk_init(self, size=1):
        super().tk_init(self.sized)

    def shape(self, canvas):
        return [
            canvas.create_oval(0, 0, self.size, self.size, width=1, outline="black", fill=self.colour)
        ]
