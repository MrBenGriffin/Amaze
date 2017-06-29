from abc import ABCMeta, abstractmethod
from Maze.cell import Cell


class Mover(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def _run(self):
        pass

    def __init__(self):
        self.track = []
        self.id = None
        self.canvas = None
        self.halo = None
        self.body = None
        self.size = Cell.size // 2
        self.offset = 10 + Cell.size // 4

    def tk_init(self, canvas):
        self.canvas = canvas
        self.id = canvas.create_oval(0, 0, self.size, self.size, outline=self.halo, fill=self.body)
        self.canvas.move(self.id, self.offset, self.offset)

    def tk_move(self, dim):
        x = dim.x * Cell.size + self.offset
        y = dim.y * Cell.size + self.offset
        self.canvas.coords(self.id, x, y, x + self.size, y + self.size)

    def tk_paint(self):
        self._run()
        if self.track:
            self.tk_move(self.track[-1].dim)
