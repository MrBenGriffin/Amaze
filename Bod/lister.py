import random
from Bod.mover import Mover


class Lister(Mover):
    """
    An alternative to the Miner.
    So.
        (1) Compile a list of cells that I know about (have visited).
        (2) Choose a cell at random from the list.
        (3) Knock a wall out if there is one, else remove it from the list.
    """
    def __init__(self, maze):
        super().__init__(maze)
        self.is_miner = True
        self.halo = "yellow"
        self.body = "green"

    def _run(self):
        the_wall = None
        while self.track and the_wall is None:
            cell_index = random.randrange(len(self.track))
            this_cell = self.track[cell_index]
            walls_to_dig = this_cell.walls_that_can_be_dug()
            if walls_to_dig:
                the_wall = random.choice(walls_to_dig)
                next_cell = this_cell.make_door_in(the_wall)
                if next_cell:
                    self.track.append(next_cell)
                else:
                    the_wall = None
            else:
                del self.track[cell_index]

