from tkinter import *


class Config:

    def __init__(self, tk_root, action_on_submit):
        # Small Tough
        self.maze_width = 70
        self.maze_height = 10
        self.maze_levels = 4
        self.cell_size = 48

        # Good Starter
        self.maze_width = 35
        self.maze_height = 5
        self.maze_levels = 3
        self.cell_size = 40

        # self.maze_width = 54
        # self.maze_height = 8
        # self.maze_levels = 4
        # self.cell_size = 96

        # Good Medium
        # self.maze_width = 54
        # self.maze_height = 8
        # self.maze_levels = 4
        # self.cell_size = 60

        self.action_on_submit = action_on_submit
        self._root = tk_root
        self._root.title("Maze Config")

        self._frame = Frame(self._root)
        self._frame.grid(columns=3, rows=6)
        self.valid = self._frame.register(
            lambda text, i, action:
            action != '1' or text[int(i)].isdigit() and 0 < int(text) < 250
        )

        # self._show_dig = BooleanVar()
        # self._show_dig.set(False)
        # self._maze_show_dig = Checkbutton(self._frame, anchor=W, text="Show Digging",
        #                                   variable=self._show_dig)

        self._maze_width_label = Label(self._frame, text="Maze Width")
        self._maze_width_entry = Entry(self._frame, validate="key",
                                       validatecommand=(self.valid, '%P', '%i', '%d'))

        self._maze_height_label = Label(self._frame, text="Maze Height")
        self._maze_height_entry = Entry(self._frame, validate="key",
                                        validatecommand=(self.valid, '%P', '%i', '%d'))

        self._maze_levels_label = Label(self._frame, text="Maze Levels")
        self._maze_levels_entry = Entry(self._frame, validate="key",
                                        validatecommand=(self.valid, '%P', '%i', '%d'))

        self._maze_size_label = Label(self._frame, text="Maze Cell Size")
        self._maze_size_entry = Entry(self._frame, validate="key",
                                      validatecommand=(self.valid, '%P', '%i', '%d'))

        self._miner = Button(self._frame, text="Miner", command=self._do_miner)
        self._lister = Button(self._frame, text="Lister", command=self._do_lister)
        self._slaver = Button(self._frame, text="Slaver", command=self._do_slaver)

        self._root.bind('<Return>', (lambda e, b=self._slaver: b.invoke()))

        self._maze_width_entry.insert(END, self.maze_width)
        self._maze_height_entry.insert(END, self.maze_height)
        self._maze_size_entry.insert(END, self.cell_size)
        self._maze_levels_entry.insert(END, self.maze_levels)

        self._maze_width_label.grid(row=0, column=0, sticky=E)
        self._maze_width_entry.grid(row=0, column=1, columnspan=2)
        self._maze_height_label.grid(row=1, column=0, sticky=E)
        self._maze_height_entry.grid(row=1, column=1, columnspan=2)
        self._maze_levels_label.grid(row=2, column=0, sticky=E)
        self._maze_levels_entry.grid(row=2, column=1, columnspan=2)
        self._maze_size_label.grid(row=3, column=0, sticky=E)
        self._maze_size_entry.grid(row=3, column=1, columnspan=2)

        # self._maze_show_dig.grid(row=4, columnspan=3)
        self._miner.grid(row=5, column=0)
        self._lister.grid(row=5, column=1)
        self._slaver.grid(row=5, column=2)

    def place(self, x, y):
        self._frame.place(x, y)

    def _do_miner(self):
        self._get_size(1)

    def _do_lister(self):
        self._get_size(2)

    def _do_slaver(self):
        self._get_size(3)

    def _get_size(self, digger):
        show_dig = True  # self._show_dig.get()
        width = int('0' + self._maze_width_entry.get())
        height = int('0' + self._maze_height_entry.get())
        levels = int('0' + self._maze_levels_entry.get())
        cell_size = int('0' + self._maze_size_entry.get())
        if width and height and cell_size:
            self.action_on_submit(width, height, levels, cell_size, digger, show_dig)


if __name__ == "__main__":
    root = Tk()
    app = Config(root, None)
    root.mainloop()
