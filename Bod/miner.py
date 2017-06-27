import random


class Miner:
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

    This is a nice bit of tail-recursion, so there is absolutely no reason why Python should balk,
    as tail-recursion can be optimised very easily by modern static analysis.
    """

    def dig(self, this_cell):
        """ Dig a maze starting from a cell """
        walls_to_dig = this_cell.walls_that_can_be_dug()
        if walls_to_dig:
            walls_list = list(walls_to_dig)
            random.shuffle(walls_list)      # Interesting to see when this line is commented out.
            for the_wall in walls_list:
                if walls_to_dig[the_wall].can_be_dug():
                    next_cell = this_cell.make_door_in(the_wall)
                    self.dig(next_cell)
