from Bod.mover import Mover
from Maze.util import Com

class Gamer(Mover):
    moving = Com.X

    def __init__(self, maze):
        super().__init__(maze)
        self.moving = Com.X
        self.halo = "white"
        self.body = "blue"

    def move(self, com):
        this_cell = self.track.pop()
        next_cell = this_cell.move(com, self.keys)
        if this_cell != next_cell:
            exits = next_cell.exits()
            if len(exits) > 2:
                self.moving = Com.X
            else:
                if len(exits) == 2:
                    # This moves us up and down levels too...
                    exits.remove(com.opposite)
                    self.moving = exits.pop()
        self.canvases[next_cell.level.level].focus_set()
        self.track.append(next_cell)
        self.tk_move(next_cell.dim)

    def move_n(self, _):
        self.moving = Com.N

    def move_s(self, _):
        self.moving = Com.S

    def move_w(self, _):
        self.moving = Com.W

    def move_e(self, _):
        self.moving = Com.E

    def move_c(self, _):
        self.moving = Com.C

    def move_f(self, _):
        self.moving = Com.F

    def tk_init(self, maze_levels):
        super().tk_init(maze_levels)
        for i in range(self.levels):
            self.canvases[i].bind('<KeyPress-w>', self.move_s)
            self.canvases[i].bind('<KeyPress-a>', self.move_w)
            self.canvases[i].bind('<KeyPress-s>', self.move_n)
            self.canvases[i].bind('<KeyPress-d>', self.move_e)
            self.canvases[i].bind('<Up>', self.move_c)
            self.canvases[i].bind('<Down>', self.move_f)
        self.canvases[0].focus_set()

    def _run(self):
        self.move(self.moving)
        self.moving = None
