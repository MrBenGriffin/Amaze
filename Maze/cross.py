
class Cross:
    XLXR = "━"
    TLXX = "┛"

    def __init__(self, top, left, bottom, right):
        self.cross = "╋"
        self._compose(top, left, bottom, right)

    def _compose(self, top, left, bottom, right):
        """
            Compose a character made up from 4 arms based on ╬
            So, each arm of the self.cross ╬ needs to be added/chopped
            based on those four conditions.
        """
        if right:  # R??? [╺]
            if bottom:   # RB?? [╔]
                if left:   # RBL? [╦]
                    if top:   # RBLT [╬]
                        self.cross = "╋"
                    else:  # RBLx
                        self.cross = "┳"
                else:  # RBx? ╔
                    if top:  # RBxT [╠]
                        self.cross = "┣"
                    else:  # RBxx
                        self.cross = "┏"
            else:  # Rx?? [╺]
                if left:  # RxL? [═]
                    if top:  # RxLT [╩]
                        self.cross = "┻"
                    else:  # RxLx
                        self.cross = "━"
                else:  # Rxx? [╺]
                    if top:  # RxxT [╠]
                        self.cross = "┗"
                    else:  # R
                        self.cross = "╺"
        else:   # x??? [ ]
            if bottom:   # xB??
                if left:   # xBL?
                    if top:   # xBLT
                        self.cross = "┫"
                    else:  # xBLx
                        self.cross = "┓"
                else:  # xBx?
                    if top:  # xBxT
                        self.cross = "┃"
                    else:  # xBxx
                        self.cross = "╻"
            else:  # xx?? [╺]
                if left:  # xxL?
                    if top:  # xxLT [╝]
                        self.cross = "┛"
                    else:  # xxLx
                        self.cross = "╸"
                else:  # xxx?
                    if top:  # xxxT [╠]
                        self.cross = "╹"
                    else:  # x
                        self.cross = " "

    def __str__(self):
        return self.cross

if __name__ == "__main__":
    print(Cross(True, True, True, True))
    print(Cross(True, True, True, False))
    print(Cross(True, True, False, True))
    print(Cross(True, True, False, False))

    print(Cross(True, False, True, True))
    print(Cross(True, False, True, False))
    print(Cross(True, False, False, True))
    print(Cross(True, False, False, False))

    print(Cross(False, True, True, True))
    print(Cross(False, True, True, False))
    print(Cross(False, True, False, True))
    print(Cross(False, True, False, False))

    print(Cross(False, False, True, True))
    print(Cross(False, False, True, False))
    print(Cross(False, False, False, True))
    print(Cross(False, False, False, False))

