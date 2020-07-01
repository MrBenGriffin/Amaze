# import random
from math import sqrt
from random import choice, randint

from Bod.mover import Mover
from Thing.gate import Gate
from Thing.key import Key

"""
Currently, the main path is made of A->B->C key/gate pairs, which is trivial to transit across.
So, we get key 'a', and can pass through 'A' gates.
.. with exchange, between the 'A' gate and the 'B' gate we need to find the 'b' key 

..a .. A ..a->b ... B ... b->c ... C ... c->a A, etc.

for overlapping keys (with exchange) if we don't have change-back, then there's a no return problem:
..a .. x ..    A ..a->b .. B .. X ... b->c ... C ... c->a A, etc.
  a    -       a      b    b    ! ... DEAD! (no way to get x)
  a    x       a      b    b    x ... -> no problem

..a .. x ..    A ..a->b ..  .b->a .. B .. X ... b->c ... C ... c->a A, etc.
  a    -       a   b         a (fetch x, then as below from x) 
  a    x       a   b         -       b    x ... -> no problem

for branching gates we also need a->b and b->a exchanges
..a .. A1 ..a->b ... B ... b->c ... C ... > dead end!!  
..a .. A2 ..a->b ... B ... b->c ... C ... > exit!!  

"""
class Gatemaker(Mover):
    def __init__(self, maze, worm):
        super().__init__(maze)
        self.gate_distance = 1
        self.min_key_gate_distance = 1
        self.gates = 0
        self.keys = tuple()
        self.worm = worm

    def _run(self):
        pass

    # let's try a recursive make.. (so it's.. make one good and one decoy between [in] and [out]
    def make(self, gate_count, start_cell, goal_cell):
        # we want to make a real gate between start and goal, and then some decoys also..
        # the real gate needs to be on the start=>goal path
        # the decoys need to be OFF the start=>goal path
        # decoys need to have something behind them - not just dead-ends!
        # (they also need a return key behind them)
        if gate_count > 0:  # are we still trying to make gates? if so...
            if start_cell.gate:
                key_exchange = set(start_cell.gate.unlocked_with)
            else:
                key_exchange = set()
            blocks = [start_cell, goal_cell]
            decoys = []
            master = self.worm.make_track(start_cell, goal_cell).copy()  # 'path' = path from start to goal.
            # we want the path to exclude decoys and include good one.
            master_length = len(master)
            if master_length <= 12:  # we don't want to bother with any gates if the path <=12
                return
            gate_point = master_length // 2  # we want to place the gate roughly have way between start and goal.
            # let's get all the distances for each cell within the bounds of start/goal, starting from start+1.
            main_gate = master[gate_point]
            gate_track = self.worm.make_track(start_cell, main_gate).copy()
            blocks.append(main_gate)

            decoy_paths = self._find_far(master, blocks, 12)
            if decoy_paths:
                rev_key = decoy_paths.pop()[-1]
            else:
                rev_key = None
                for i, x in enumerate(gate_track[1:-1]):
                    if x.key or x.gate:
                        if i < int(gate_point * 2/3):
                            rev_key = gate_track[i - 1]
                        break
                if not rev_key:
                    rev_key = gate_track[int(gate_point * 1/3)]
            decoy_paths = decoy_paths[:randint(3, 5)]
            for decoy in decoy_paths:
                decoys.append([decoy[0], decoy[-1]])
                blocks.append(decoy[0])

            key_paths = self._find_far(gate_track, blocks, 6)
            if key_paths:
                key_cell = key_paths[0][-1]
            else:
                key_cell = None
                for i, x in enumerate(reversed(gate_track[1:-1])):
                    if x.key or x.gate:
                        if i < int(gate_point * 1/3):
                            key_cell = gate_track[i - 1]
                        break
                if not key_cell:
                    key_cell = gate_track[int(gate_point * 2/3)]
            self._make_key(key_cell, main_gate, key_exchange.copy())
            self.make(gate_count - 1, main_gate, goal_cell)
            if start_cell.gate:
                self._make_key(rev_key, start_cell, {}, start_cell.gate.unlocked_with)
            for decoy in decoys:
                ok = True
                decoy_track = self.worm.make_track(key_cell, decoy[0]).copy()
                for cell in decoy_track[1:]:
                    if cell.key or cell.gate:
                        ok = False
                        break
                if ok:
                    decoy[0].gate = Gate(True, key_cell.key)
                    self.maze.add_thing(decoy[0], decoy[0].gate)
                    self.make(gate_count - 1, decoy[0], decoy[1])

            #branch_paths = self._find_far(master, blocks, 6)
            # if len(branch_paths) >= 2:
            #     key_cell = branch_paths.pop(0)[-1]
            #     self._make_key(key_cell, main_gate, key_exchange.copy())
            #     if start_cell.gate:
            #         rev_key = branch_paths.pop(0)[-1]
            #         self._make_key(rev_key, start_cell, {key_cell.key.name}, start_cell.gate.unlocked_with)
            #     decoy_paths = branch_paths[:randint(2, 5)]
            #     self.make(gate_count - 1, main_gate, goal_cell)
            #     for decoy in decoy_paths:
            #         decoy[0].gate = Gate(True, key_cell.key)
            #         self.maze.add_thing(decoy[0], decoy[0].gate)
            #         self.make(gate_count - 1, decoy[0], decoy[-1])

    def _find_far(self, path, stops, too_short):
        if not path:
            return []
        cell_distances = self.worm.distances(path[1], stops)  # get distance from start position.
        self.worm.cull(cell_distances)  # removes adjacent cells.
        # get a list of cell indices which are not in path
        cells = [cell for x in cell_distances.keys() for cell in cell_distances[x] if self.maze.at(cell) not in path]
        # get a path to each of them, removing anything in path.
        paths = [[t for t in self.worm.make_track(path[1], self.maze.at(c)).copy() if t not in path] for c in cells]
        result = [p for p in paths if len(p) > too_short]  # cull short paths.
        result.sort(key=lambda x: len(x), reverse=True)  # sorted them with the longest paths first
        return result

# given a list of cells, order them (and their midpoint from start) that are farthest away from both start and goal.
    def _sel_far(self, candidates, ends, stops):
        result = {}
        for candidate in candidates:
            c_cell = self.maze.at(candidate)
            a_track = self.worm.make_track(ends[0], c_cell)
            a = len(a_track)
            gate_point = a // 2
            gate = a_track[gate_point]
            while gate in stops and gate_point + 12 < a:
                gate_point += 1
                gate = a_track[gate_point]
            b = len(self.worm.make_track(c_cell, ends[1]))
            score = sqrt(a*a + b*b)
            result[score] = [c_cell, gate]
        stuff = [result[x] for x in sorted(result.keys(), reverse=True)]
        return stuff

    # This is a linear make..
    def old_make(self, gate_count, worm, start_cell, goal_cell):
        master_track = worm.make_track(start_cell, goal_cell).copy()
        track_length = len(master_track)
        key_exchange = tuple()
        self.gate_distance = max(1, track_length // gate_count)
        self.min_key_gate_distance = max(1, self.gate_distance // 3)
        leg_in = 0
        leg_out = self.gate_distance
        while leg_out < len(master_track) - 1:
            leg_a = master_track[leg_in]
            leg_b = master_track[leg_out]
            leg_start = master_track[leg_in + 1]
            # key_1 = self._choose_key_cell(worm, leg_start, [leg_a, leg_b])
            # we want two keys between leg_a and leg_b
            # they A[.. (b->a) .. (a->b) ..]B
            # gen.  [ .. R .. F .. ] (reverse/forward)
            keys = self._choose_cells(master_track, worm, leg_start, [leg_a, leg_b], 2)
            if keys:
                key_exchange = self._make_key(keys.pop(), leg_b, key_exchange)
                if leg_a.gate:
                    if keys:
                        self._make_key(keys.pop(), leg_a, key_exchange, leg_a.gate.unlocked_with)
                    else:
                        pass

            leg_in = leg_out
            leg_out += self.gate_distance

    def _choose(self, path, goal, stops, number, allow_on_path=False, choosing_gates=False, max_length=None):
        result = set()
        if path:
            a_b = self.worm.distances(path[1], stops, max_length)
            self.worm.cull(a_b)  # removes adjacent cells.
            heavies = sorted(a_b.keys(), reverse=True)
            for distance in heavies:
                cell_list = a_b[distance]
                for cell_index in cell_list:
                    contender = self.maze.at(cell_index)
                    if allow_on_path or contender not in path:
                        if not contender.gate and not contender.key:
                            key_path = self.worm.make_track(contender, goal)
                            path_len = len(key_path)
                            if path_len > self.min_key_gate_distance:
                                if choosing_gates:
                                    result.add(key_path[path_len // 2])
                                else:
                                    result.add(contender)
                if len(result) >= number:
                    break
        return result

    def _choose_cells(self, master, worm, start, stops, number, include_path=False):
        result = set()
        a_b = worm.distances(start, stops)
        worm.cull(a_b)  # removes adjacent cells.
        heavies = sorted(a_b.keys(), reverse=True)
        for distance in heavies:
            cell_list = a_b[distance]
            for cell_index in cell_list:
                contender = self.maze.at(cell_index)
                if include_path or contender not in master:
                    if not contender.gate and not contender.key:
                        key_to_gate = worm.make_track(contender, stops[-1])
                        if len(key_to_gate) > self.min_key_gate_distance:
                            result.add(contender)
            if len(result) >= number:
                break
        return result

    def _make_key(self, key_cell, gate_cell, exchange=(), name=None):
        key_cell.key = Key(gate_cell, exchange, name)
        self.maze.add_thing(key_cell, key_cell.key)
        key_cell.key.tk_init(self.maze, key_cell)
        if not gate_cell.gate:
            gate_cell.gate = Gate(True, key_cell.key)
            self.maze.add_thing(gate_cell, gate_cell.gate)
        return tuple(key_cell.key.name)
