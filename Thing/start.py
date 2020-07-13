from Thing.item import Item

class Start(Item):

    def __init__(self, cell):
        super().__init__()
        self.cell = cell

    def tk_init(self, size=1.0):
        super().tk_init(size)

    def shape(self, canvas):
        fill_colour = "#AAA"
        text_offset = self.cell.size - self.cell.size * 0.50
        text_scale = int(self.cell.size * 0.33)

        return [
            canvas.create_rectangle(0, 0, self.size, self.size, width=0, fill=fill_colour),
            canvas.create_text(text_offset, text_offset, font=("Monaco", text_scale, 'bold'), text='Start', fill='white')
        ]
