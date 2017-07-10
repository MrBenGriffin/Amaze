from Bod.mover import Mover
from Maze.util import Com


class Goal(Mover):
    def __init__(self):
        super().__init__()
        self.halo = "red"
        self.body = "orange"

    def _run(self):
        pass


class Gamer(Mover):
    def __init__(self):
        super().__init__()
        self.halo = "white"
        self.body = "blue"

    def move(self, com):
        this_cell = self.track.pop()
        next_cell = this_cell.move(com)
        self.canvases[next_cell.level.level].focus_set()
        self.track.append(next_cell)
        self.tk_move(next_cell.dim)

    def move_n(self, _):
        self.move(Com.N)

    def move_s(self, _):
        self.move(Com.S)

    def move_w(self, _):
        self.move(Com.W)

    def move_e(self, _):
        self.move(Com.E)

    def move_c(self, _):
        self.move(Com.C)

    def move_f(self, _):
        self.move(Com.F)

    def tk_init(self, maze_levels):
        super().tk_init(maze_levels)
        for i in range(self.levels):
            self.canvases[i].bind("w", self.move_s)
            self.canvases[i].bind("a", self.move_w)
            self.canvases[i].bind("s", self.move_n)
            self.canvases[i].bind("d", self.move_e)
            self.canvases[i].bind("q", self.move_c)
            self.canvases[i].bind("e", self.move_c)
            self.canvases[i].bind("c", self.move_f)
            self.canvases[i].bind("x", self.move_f)
        self.canvases[0].focus_set()

    def _run(self):
        pass
