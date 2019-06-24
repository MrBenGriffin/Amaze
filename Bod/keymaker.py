import random
from Bod.mover import Mover
from Thing.key import Key


class Keymaker(Mover):
    def __init__(self, maze):
        super().__init__(maze)
        self.dead_ends = []

    def _run(self):
        if self.track:
            this_cell = self.track[-1]
            cell = None
            exits = this_cell.exits()
            while exits and not cell:
                cell = this_cell.move(exits.pop())
                if cell in self.track or cell == self.goal or cell in self.dead_ends:
                    cell = None
            if cell:
                self.track.append(cell)
            else:
                self.dead_ends.append(self.track.pop())

    def finished(self):
        return not self.track

    def set_key(self):
        if self.goal in self.dead_ends:
            self.dead_ends.remove(self.goal)
        if self.dead_ends:
            self.maze.add_thing(random.choice(self.dead_ends), Key())
            return True
        else:
            return False
