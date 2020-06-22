# encoding: utf-8
from tkinter import Canvas, Label, StringVar
from Maze.level import Level
from Maze.cell import Cell

class Maze:
    """
        Maze is created as a rectangle (cuboid) of x * y (*z) cells.
        Each Maze is made of 1...X levels.
        Each Maze level has it's own Canvas..
        For the time being, each level uses the same dimensions..
        (Not hard to change this).

    """
    start = (0, 0, 0)

    def __init__(self, cells_across, cells_up, depth, cell_size):
        self.gates = 0
        self.cells_across = cells_across
        self.cells_up = cells_up
        self.depth = depth
        self.space = 20
        self.offset = self.space // 2
        self.mined = False
        self.tk_maze = None
        self.tk_status = None
        self.bods = []
        self.bod_icons = []
        self.things = []
        self.levels = []
        # print("Making maze:", cells_across, cells_up, depth)
        for level in range(self.depth):
            floor = Level(cells_across, cells_up, cell_size, level)
            self.levels.append(floor)
        for level in self.levels:
            level.set_floor(self)

    def do_mined(self):
        # This happens just once after the miners are done.
        # So we can post-process the mine here.
        self.mined = True
        for level in self.levels:
            level.erode()

    def at(self, index):
        return self.cell(index[0], index[1], index[2])

    def cell(self, cells_across, cells_up, level=None):
        if level is None or level not in range(0, self.depth):
            return None
        return self.levels[level].cell(cells_across, cells_up)

    def add_thing(self, cell: object, thing: object) -> object:
        if self.tk_maze:
            from Thing.gate import Gate
            if isinstance(thing, Gate):
                self.gates += 1
            self.things.append(thing)
            thing.tk_init(self, cell)

    def add_bod(self, bod):
        self.bods.append(bod)
        bod.tk_init(self)

    def remove_bod(self, bod):
        self.bods.remove(bod)
        bod.tk_init(self)

    def mine(self, bod, show):
        while not bod.finished():
            bod.run()
            self.do_mined()

    def tk_init_maze(self, maze_window):
        self.tk_maze = maze_window
        self.tk_maze.title("Maze")
        for level in self.levels:
            level.tk_level = Canvas(self.tk_maze,
                                    width=  self.space + Cell.size * (self.cells_across + 0),
                                    height= self.space + Cell.size * (self.cells_up + 0),
                                    bg='gray')
            level.tk_level.grid(columns=1, rows=1)
        self.tk_maze.after(0, self.animation)

    def tk_init_bods(self, bods_window):
        self.tk_status = bods_window
        self.tk_status.title("Status")
        row_id = 0
        for bod in self.bods:
            icon = Canvas(self.tk_status, width=Cell.size, height= Cell.size, bg='gray')
            # bod.tk_status =
            icon.grid(row=row_id, column=0)
            bod.tk_object(icon)
            key_label = Label(self.tk_status, text="Keys:").grid(row=row_id, column=1)
            key_text = StringVar()
            key_text.set("-")
            key_list = Label(self.tk_status, textvariable=key_text).grid(row=row_id, column=2)
            bod.tk_status = [icon, key_text, key_label, key_list]
            row_id += 1
        self.tk_status.after(0, self.status_update)

    def animation(self):
        for bod in self.bods:
            if bod.is_miner:
                if not self.mined:
                    bod.tk_paint()
            else:
                if self.mined:
                    bod.tk_paint()
        for thing in self.things:
            thing.tk_paint()
        self.tk_maze.after(60, self.animation)

    def status_update(self):
        for bod in self.bods:
            bod.tk_paint_status()
        self.tk_status.after(60, self.status_update)

    def tk_paint(self):
        for level in self.levels:
            level.tk_paint()

    def string(self):
        result = ""
        for level in self.levels:
            result += level.string()
        return result


