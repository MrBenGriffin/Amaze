import random
from Bod.mover import Mover


class Miner(Mover):
    """
    Miner is a simple solitary random walk algorithm.
    The miner starts at a cell in the mine, then chooses a wall to knock down.
    Mining Rule #1 is that he cannot knock down a wall into a pre-visited cell.
    When he gets to a dead end (all the surrounding cells are visited or are edges) then
    he backtracks to the previous cell he visited.

    So.
        (1) Get a dict of walls that I can dig from my current cell.
        (2) If the dict isn't empty, shuffle the list (actually just the keys).
        (3) and then for each, check it still can be dug (because we are recursive).
        (4) and it it can be dug, dig it and move there, marking where I've come from, and go to (1)
        (6) continue the good work from my previous cell..
        This is now not doing any recursion. The only state kept is the cell, which is put onto a
        local stack (called self.track) instead. This now allows us to animate the Miner.

    """
    def __init__(self):
        super().__init__()
        self.halo = "green"
        self.body = "white"

    def _run(self):
        """
        adding the while with the_wall test means that we don't get to SEE backtracking
        when we are animating the miner.
        """
        the_wall = None
        while self.track and the_wall is None:
            this_cell = self.track[-1]
            walls_to_dig = this_cell.walls_that_can_be_dug()
            if walls_to_dig:
                the_wall = random.choice(list(walls_to_dig))
                next_cell = this_cell.make_door_in(the_wall)
                self.track.append(next_cell)
            else:
                self.track.pop()

    def dig(self, cell):
        self.track.append(cell)
