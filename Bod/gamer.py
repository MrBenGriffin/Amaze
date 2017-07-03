from Bod.mover import Mover
from Maze.util import Com


class Goal(Mover):
    def __init__(self):
        super().__init__()
        self.halo = "red"
        self.body = "orange"

    def _run(self):
        self.go(self.track[-1])


class Gamer(Mover):
    def __init__(self):
        super().__init__()
        self.halo = "white"
        self.body = "blue"

    def move(self, com):
        this_cell = self.track.pop()
        next_cell = this_cell.move(com)
        next_cell = next_cell.stairs()
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

    def tk_init(self, maze_levels):
        super().tk_init(maze_levels)
        for i in range(self.levels):
            self.canvases[i].bind("w", self.move_s)
            self.canvases[i].bind("a", self.move_w)
            self.canvases[i].bind("s", self.move_n)
            self.canvases[i].bind("d", self.move_e)
        self.canvases[0].focus_set()

    def _run(self):
        pass
