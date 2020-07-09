import random
from Bod.mover import Mover

class Slaver(Mover):
    """
    An alternative (hybrid) to the Miner/Lister.
    This is because lister gives lots of single-cell corridors * yuck *
        (1) Act like the Miner for 16 (or 32) turns.
        (2) Act like the Lister for 1 turn.
    """

    def __init__(self, maze):
        super().__init__(maze)
        self.is_miner = True
        self.halo = "white"
        self.body = "black"
        self.sequence = 0
        self.forward = 0

    def _run(self):
        self.sequence += 1
        the_wall = None
        while self.track and the_wall is None:
            if self.sequence & 15 != 0:   # cheaper than % 16
                this_cell = self.track[-1]
                walls_to_dig = this_cell.walls_that_can_be_dug()
                if walls_to_dig:
                    the_wall = self.do_mine(walls_to_dig, this_cell)
                else:
                    self.forward = 0
                    self.track.pop()
            else:
                self.forward = 0
                cell_index = random.randrange(len(self.track))
                this_cell = self.track[cell_index]
                walls_to_dig = this_cell.walls_that_can_be_dug()
                if walls_to_dig:
                    the_wall = self.do_mine(walls_to_dig, this_cell)
                else:
                    del self.track[cell_index]

    def do_mine(self, walls_to_dig, this_cell):
        the_wall = random.choice(walls_to_dig)
        next_cell = this_cell.make_door_in(the_wall)
        if next_cell:
            self.track.append(next_cell)
            self.forward += 1
        else:
            the_wall = None
        return the_wall
