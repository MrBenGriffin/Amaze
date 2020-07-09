# encoding: utf-8
from random import shuffle
from tkinter import HIDDEN
from Maze.cell import Cell
from Maze.util import Dim, Com, Orientation


class Concrete:
    kinds = (
        (' ', '╴', '╶', '─', '╵', '┘', '└', '┴', '╷', '┐', '┌', '┬', '│', '┤', '├', '┼'),
        (' ', '╸', '╺', '━', '╹', '┛', '┗', '┻', '╻', '┓', '┏', '┳', '┃', '┫', '┣', '╋'),
        (' ', '╸', '╺', '═', '╹', '╝', '╚', '╩', '╻', '╗', '╔', '╦', '║', '╣', '╠', '╬')
    )

    def __init__(self, value=0, kind=1):
        self.corner = Concrete.kinds[kind][value & 0x0F]

    def __repr__(self):
        return self.corner


class Corner:
    def __init__(self, wall_dict):
        self.concrete = None
        self.walls = wall_dict  # N,E,S,W

    def __str__(self):
        value = Com.X
        for com, wall in self.walls.items():
            if wall and wall.is_wall():
                value |= com
        return str(Concrete(value))


class Wall:
    # following statics are used for text-drawing.
    prev_ew = False

    solids = {
        Orientation.NS: (0, 0, 1, 0),
        Orientation.EW: (0, 1, 0, 0)
    }

    def __init__(self, orientation, x, y, level):
        self.level = level
        self.blocked = False
        self.id = None
        self.x = x
        self.y = y
        self.door = "▦"
        self.cells = {}
        # We need the orientation in order to draw the right wall..
        self.orientation = orientation

        self.solid = tuple(10 + Cell.size * i + Cell.size * j for i, j in zip(
            Wall.solids[self.orientation],
            (self.x, self.y, self.x, self.y)
        ))

    def make_door(self, cell_dir, kind=None):
        if cell_dir not in self.cells:
            return None
        other = self.cells[cell_dir]
        if not self.blocked and other:
            other.mined = True
            if self.level.tk_level:
                self.level.tk_level.itemconfig(self.id, state=HIDDEN)
            if kind is None:
                self.door = " "
            else:
                self.door = kind
            return other
        else:
            return None

    def erode(self):
        if self.is_wall():
            pass

    def make_solid(self):
        self.door = "▦"

    def is_wall(self) -> bool:
        return self.door == "▦"

    def set_cell(self, cell, com):
        self.cells[com] = cell
        opp = com.opposite
        if opp not in self.cells:
            self.cells[opp] = None

    def is_edge(self):  # If on the edge, then one of my wall cells will be None.
        if self.orientation == Orientation.NS:
            return (self.cells[Com.N] is None) or (self.cells[Com.S] is None)
        else:
            return (self.cells[Com.W] is None) or (self.cells[Com.E] is None)

    def can_be_dug(self, com_from):
        cell = self.cells[com_from]
        return not self.blocked and cell and not cell.mined

    def __str__(self):
        if not self.is_wall():
            return ' '
        if self.orientation == Orientation.NS:
            return str(Concrete(Com.E | Com.W))
        return str(Concrete(Com.N | Com.S))

    def tk_paint(self):
        if self.level.tk_level:
            if self.is_wall():
                self.id = self.level.tk_level.create_line(self.solid, width=2)
            else:
                self.id = self.level.tk_level.create_line(self.solid, width=2, state=HIDDEN)


class Floor:
    """
    Represents a 'floor' between two cells.
    The cell floor is the lower cell's ceiling.
    the Com.C is the cell that sees this as a ceiling.
    the Com.F is the cell that sees this as a floor.
    """
    id = ['💙', '🌔', '️🐿', '🕷', '🎹️', '🐴', '🌀', '🥨', '🐖', '🐣', '📗', '🐏', '🌲', '🐤', '⛏',
          '🤩', '😂', '🦄', '️💌', '🦑', '🌱️', '🥑', '️🛷', '😴', '🥄', '️🌈', '💣', '🦁', '😱', '🌒',
          '🐔', '👣', '🍉️', '💟', '🌕', '🔥', '😜', '🐱', '🦊', '️🚚', '🟫', '🌖️', '🔴', '🥳', '💣️',
          '🔵', '💧', '😘', '🍎', '😈', '🟠', '😃', '🦅', '🌜', '🐼', '🦢', '🧵', '🐬', '🐰', '🌑',
          '🌏', '🏡', '🌎', '🦆', '🐗', '🦞', '🎃', '🪐', '🦉', '🧩', '🐝', '️🤖', '🌚', '😸', '🍄',
          '🍇️', '🟤', '💥', '💛', '📕', '📒', '😍', '🐵', '🐺', '️👓', '🦇', '⚙️', '💩', '🌴', '🐮',
          '🙂', '️🎉', '✈️', '🤓', '🐠', '🌙', '👻', '🍪', '👁', '🥺', '🐷', '🌝', '🍕️', '🟢', '📘',
          '🐪', '🍩', '🦴', '️🎸', '🦔', '⏱', '✳️', '🐭', '⛄️', '🐨', '🧲', '🤣', '️🐫', '🤪', '🧡',
          '🔶️', '🐦', '⚓️', '📙', '😎', '😞', '⛳️', '💈️', '🌛', '🐳', '🐉', '🛠', '🌘', '😇', '🥶️',
          '🕸', '️👹', '💰', '🔔', '💜', '🐧', '🔷', '️🕰', '😭', '🐸', '️📎', '🌓', '🏆️', '🚗', '️😍',
          '🐯', '💚', '🌞', '🌗', '🐻', '🐹', '🎡', '🐙', '🥰', '🌍️', '🍪️', '🏹', '🎲', '🛴', '🏖']

    # ids = len(id)
    shuffle(id)
    _id_ptr = 0

    def __init__(self, floor, ceiling):
        self.cells = {Com.C: ceiling, Com.F: floor}
        self.solid = True
        self.id = None
        self.tk_c = self.tk_f = None
        if ceiling:
            ceiling.floors[Com.C] = self
        floor.floors[Com.F] = self
        t = floor.walls[Com.N].solid
        b = floor.walls[Com.S].solid
        self.p = Dim(b[0] + 4, t[1] - 4, 0)
        self.q = Dim(b[2] - 4, b[1] + 4, 0)

    def make_hole(self, com):
        other = self.cells[com.opposite]
        if self.solid and other.floors[com.opposite].solid:
            self.solid = False
            self._set_id()
            self._shape()
        return other

    def _set_id(self):
        self.id = Floor.id[Floor._id_ptr]
        Floor._id_ptr += 1

    def _tkbit(self, cell):
        if cell.level.tk_level:
            ox = cell.dim.x * cell.size + cell.level.maze.offset
            oy = cell.dim.y * cell.size + cell.level.maze.offset
            text_offset = cell.size - cell.size * 0.8
            text_scale = int(cell.size * 0.8)
            text_delta = int(cell.size * 0.25)
            cell.level.tk_level.create_text(
                ox + text_offset + text_delta,
                oy + text_offset + text_delta,
                font=("*", text_scale), text=f"  {self.id}")

    def _shape(self):
        if self.solid:
            return
        for k in self.cells:
            self._tkbit(self.cells[k])
