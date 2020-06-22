# import random
from random import choice

from Bod.mover import Mover
# from Thing.key import Key
from Thing.gate import Gate
from Thing.key import Key

"""
    We should really run a separate gate-maker, which first of all goes from start to goal,
    and then uses the track (or a track if there's not just one) to put gates on.
    Then, [->...A....B....C....->]. Then add kA somewhere between start and A,
    kB somewhere between start and B, kC somewhere between start and C .. etc.
    For key exchanges, (eg A->C) that must be placed between A and C rather than start and C.
    Once a key has been exchanged, it can be re-used.
    ka A ka->kc, kb B ka C ka A, kb->e E
"""
class Gatemaker(Mover):
    def __init__(self, maze):
        super().__init__(maze)
        self.master_track = None
        self.gate_distance = 1
        self.min_key_gate_distance = 1

    def _run(self):
        pass

    def make(self, gate_count, worm, start_cell, goal_cell, cell_distances):
        self.master_track = worm.make_track(start_cell, goal_cell).copy()
        track_length = len(self.master_track)
        self.gate_distance = max(1, track_length // gate_count)
        self.min_key_gate_distance = max(1, self.gate_distance // 3)
        leg_in = 0
        leg_out = self.gate_distance
        while leg_out < len(self.master_track) - 1:
            leg_a = self.master_track[leg_in]
            leg_b = self.master_track[leg_out]
            leg_start = self.master_track[leg_in + 1]
            key_c = self._choose_key_cell(worm, leg_start, [leg_a, leg_b])
            if key_c:
                self._make_key(key_c, leg_b)
            leg_in = leg_out
            # if not leg_b.gate.bi_directional:
            #     leg_in = leg_out
            leg_out += self.gate_distance

    def _choose_key_cell(self, worm, start, stops):
        a_b = worm.distances(start, stops)
        heavy_first = reversed(sorted(a_b.keys()))
        for distance in heavy_first:
            cell_list = a_b[distance]
            for cell_index in cell_list:
                if cell_index not in self.master_track:
                    contender = self.maze.at(cell_index)
                    if not contender.gate and not contender.key:
                        key_to_gate = worm.make_track(contender, stops[-1])
                        if len(key_to_gate) > self.min_key_gate_distance:
                            return contender
        return None

    def _make_key(self, key_cell, gate_cell):
        key_cell.key = Key(gate_cell)
        self.maze.add_thing(key_cell, key_cell.key)
        key_cell.key.tk_init(self.maze, key_cell)
        gate_cell.gate = Gate(True, key_cell.key)
        self.maze.add_thing(gate_cell, gate_cell.gate)
