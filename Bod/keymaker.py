import random
from Bod.mover import Mover
from Thing.key import Key


class Keymaker(Mover):
    def __init__(self, maze):
        super().__init__(maze)
        self.dead_ends = []
        self.contenders = []
        self.min_gates = self.maze.gates - 1
        self.cur_gates = 0

    def _run(self):
         if self.track:
            this_cell = self.track[-1]
            cell = None
            exits = this_cell.exits()
            while exits and not cell:
                cell = this_cell.move(exits.pop(), self.keys)
                if cell in self.track or cell in self.dead_ends:
                    cell = None
            if cell:
                if cell == self.goal:
                    self.track.clear()
                else:
                    if cell.gate:
                        self.cur_gates += 1
                    self.track.append(cell)
            else:
                contender = self.track.pop()
                self.dead_ends.append(contender)
                if self.cur_gates >= self.min_gates:
                    if not contender.key and not contender.gate and not contender.stairs():
                        self.contenders.append(contender)

    def finished(self):
        return not self.track

    def make_key(self, gate_cell):
        if self.goal in self.contenders:
            self.contenders.remove(self.goal)
        if self.contenders:
            key_cell = random.choice(self.contenders)
            key_cell.key = Key(gate_cell)
            self.keys.add(key_cell.key.name)
            self.maze.add_thing(key_cell, key_cell.key)
            key_cell.key.tk_init(self.maze, key_cell)
            return key_cell
        else:
            return None
