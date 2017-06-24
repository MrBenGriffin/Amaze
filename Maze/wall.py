# encoding: utf-8
""""
    Not knowing anything about Python, here is a simple Wall class that
    should represent what we need to know about Walls.
    There are two aspects to a wall in general, one is which direction it is going in
    (north-south) or (west-east) - and then whether or not it has a doorway in it.

    I have also added a simple 'enum' class for Orientation. It's possibly a bit OTT.
"""


class Orientation:
    NS = True
    EW = False

    def __init__(self):
        pass


class Wall:
    def __init__(self, orientation=None, has_door=None):
        if has_door is None:
            self.door = False
        else:
            self.door = has_door

        if orientation is None:
            self.orientation = Orientation.NS
        else:
            self.orientation = orientation

    def make_door(self):
        self.door = True

    def make_solid(self):
        self.door = False

    def __str__(self):
        if self.orientation == Orientation.NS:
            if self.door:
                return " "
            else:
                return "━"
        else:
            if self.door:
                return " "
            else:
                return "┃"
