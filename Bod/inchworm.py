from Bod.mover import Mover

class Inchworm(Mover):
    """
    Inchworm measures distances between two different positions.
    It can also find the furthest cell from another cell.
    """

    def __init__(self, maze):
        super().__init__(maze)
        self.dead_ends = []
        self.stops = []

    def _reset(self):
        self.keys.clear()
        self.dead_ends = []
        self.track.clear()
        self.stops = []

    def make_track(self, start, finish):
        self._reset()
        self.go(start)
        self.goal = finish
        while self.track and self.track[-1] != self.goal:
            self._traverse()
        return self.track

    def distances(self, start, stops=[]):
        self._reset()
        log = {start.dim.tuple(): 0}
        self.stops = stops
        self.go(start)
        while self.track and self.track[-1] not in self.stops:
            self._traverse()
            if self.track:
                last_cell = self.track[-1].dim.tuple()
                if last_cell not in log:
                    log[last_cell] = len(self.track) - 1
        result = {v: [] for v in log.values()}
        for k in log:
            result[log[k]].append(k)
        return result

    def _traverse(self):
        this_cell = self.track[-1]
        exits = this_cell.exits()
        next_cell = None
        while exits and not next_cell:
            next_cell = this_cell.move(exits.pop(), self.keys)
            if next_cell in self.track or next_cell in self.dead_ends or next_cell in self.stops:
                next_cell = None
        if next_cell:
            self.track.append(next_cell)
        else:
            self.dead_ends.append(self.track.pop())

    def _run(self):
        self._reset()
        pass
