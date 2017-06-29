from tkinter import Tk, Frame, Label, Entry, Button, E


class Config:
    def __init__(self, tk_root, action_on_submit):
        self.action_on_submit = action_on_submit
        self._root = tk_root
        self._root.title("Maze Config")
        self._frame = Frame(self._root)
        self._frame.grid(columns=2, rows=4)
        self.valid = self._frame.register(
            lambda text, i, action:
            action != '1' or text[int(i)].isdigit() and 0 < int(text) < 250
        )
        self._maze_width_label = Label(self._frame, text="Maze Width")
        self._maze_width_entry = Entry(self._frame, bd=3, validate="key",
                                       validatecommand=(self.valid, '%P', '%i', '%d'))
        self._maze_height_label = Label(self._frame, text="Maze Height")
        self._maze_height_entry = Entry(self._frame, bd=3, validate="key",
                                        validatecommand=(self.valid, '%P', '%i', '%d'))
        self._maze_size_label = Label(self._frame, text="Maze Cell Size")
        self._maze_size_entry = Entry(self._frame, bd=3, validate="key",
                                      validatecommand=(self.valid, '%P', '%i', '%d'))
        self._submit = Button(self._frame, text="Submit", command=self._get_size)

        self._maze_width_label.grid(row=0, column=0, sticky=E)
        self._maze_width_entry.grid(row=0, column=1)
        self._maze_height_label.grid(row=1, column=0, sticky=E)
        self._maze_height_entry.grid(row=1, column=1)
        self._maze_size_label.grid(row=2, column=0, sticky=E)
        self._maze_size_entry.grid(row=2, column=1)
        self._submit.grid(row=3, columnspan=2)

    def _get_size(self):
        maze_width = int('0' + self._maze_width_entry.get())
        maze_height = int('0' + self._maze_height_entry.get())
        maze_cell_size = int('0' + self._maze_size_entry.get())
        if maze_height and maze_width and maze_cell_size:
            self.action_on_submit(maze_width, maze_height, maze_cell_size)

if __name__ == "__main__":
    root = Tk()
    app = Config(root, None)
    root.mainloop()
