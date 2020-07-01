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

    # measure all distances from the start point. Do not include or go beyond stops.
    def distances(self, start, stops=[], maximum=None) -> dict:
        self._reset()
        log = {start.dim.tuple(): 0}
        self.stops = stops
        self.go(start)
        while self.track and self.track[-1] not in self.stops and (not maximum or len(self.track) <= maximum):
            self._traverse()
            if self.track:
                last_cell = self.track[-1].dim.tuple()
                if last_cell not in log:
                    log[last_cell] = len(self.track) - 1
        result = {v: [] for v in log.values()}
        for k in log:
            result[log[k]].append(k)
        return result

    def cull(self, distances):
        sorted_keys = sorted(distances.keys())
        for k in sorted_keys:
            if distances[k] and k + 1 in distances and distances[k + 1]:
                non_adjacent = []
                higher = distances[k+1]
                for d in distances[k]:
                    found = False
                    neighbours = self.maze.at(d).neighbours()
                    for neighbour in neighbours:
                        idx = neighbour.dim.tuple()
                        if idx in higher:
                            found = True
                    if not found:
                        non_adjacent.append(d)
                if non_adjacent:
                    distances[k] = non_adjacent
                else:
                    del distances[k]


        # for key in range(number):
        #     for distance in heavy_first:
        #         cell_list = a_b[distance]
        #         for cell_index in cell_list:
        #             if cell_index not in self.master_track:
        #                 contender = self.maze.at(cell_index)
        #                 if not contender.gate and not contender.key:
        #                     key_to_gate = worm.make_track(contender, stops[-1])
        #                     if len(key_to_gate) > self.min_key_gate_distance:
        #                         result.append(contender)
        # return result


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
