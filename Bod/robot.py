from Bod.mover import Mover


class Robot(Mover):
    def __init__(self, maze):
        super().__init__(maze)

        self.speed = 30
        self.tick = 0
        self.halo = "black"
        self.body = "cyan"
        self.dead_ends = []

    def _run(self):
        self.tick += 1
        if (self.track and self.tick % self.speed) == 0:
            this_cell = self.track[-1]
            cell = None
            exits = this_cell.exits()
            while exits and not cell:
                cell = this_cell.move(exits.pop(), self.keys)
                if cell in self.track or cell in self.dead_ends:
                    cell = None
            if cell:
                self.track.append(cell)
            else:
                self.dead_ends.append(self.track.pop())
