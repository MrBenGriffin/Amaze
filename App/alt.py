from math import floor, ceil

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QGraphicsScene
from PyQt5.QtCore import Qt, QRect


class Wall:
    def __init__(self):
        pass

class Maze:
    def __init__(self):
        self.x = 1
        self.y = 1
        self.z = 1
        self.cells = {}
        self.scenes = []

    def reset(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        self.cells = {tuple((ix, iy, iz)): (True, True, True, True, True, True)  # N S E W C F
                      for ix in range(self.x)
                      for iy in range(self.y)
                      for iz in range(self.z)
                      }
        for scene in self.scenes:
            scene.clear()

    def draw(self, offset, scale):
        len = scale
        for x, y, z in self.cells:
            cx1 = offset + x * scale
            cy1 = offset + y * scale
            cx2 = cx1 + len
            cy2 = cy1 + len
            walls = self.cells[x, y, z]
            if walls[0]:
                self.scenes[z].addLine(cx1, cy1, cx2, cy1)
            if walls[1]:
                self.scenes[z].addLine(cx2, cy1, cx2, cy2)
            if walls[2]:
                self.scenes[z].addLine(cx1, cy2, cx2, cy2)
            if walls[3]:
                self.scenes[z].addLine(cx1, cy1, cx1, cy2)

class MyDialog(QtWidgets.QDialog):

    def __init__(self, form):
        self.form = form
        self.horizontal_layout = None
        self.offset = 12
        self.demi = self.offset // 2
        self.tmp_idx = 0
        self.levels = 4
        self.width = 6
        self.height = 7
        self.cell_size = 48
        self.maze = None
        self.level_tabs = []
        self.level_gx = []
        self.tab_widget = None
        super().__init__()

    def reset_tab(self):
        self.tmp_idx = 0
        prev_widget = self.tab_widget
        self.tab_widget = QtWidgets.QTabWidget(self)
        if prev_widget:
            self.tmp_idx = prev_widget.currentIndex()
            self.horizontal_layout.replaceWidget(prev_widget, self.tab_widget)
            prev_widget.clear()
            prev_widget.close()
        else:
            self.horizontal_layout.addWidget(self.tab_widget)
        self.tab_widget.setMinimumSize(QtCore.QSize(310, 380))
        self.tab_widget.setTabPosition(QtWidgets.QTabWidget.North)
        self.tab_widget.setObjectName("tab_widget")
        if self.maze:
            for lt in self.level_tabs:
                lt.close()
            self.level_tabs = []
            for gx in self.level_gx:
                gx.close()
            self.level_gx = []
            self.maze.scenes = []

    def draw_maze(self, geometry):
        self.reset_tab()
        for level in range(self.levels):
            tab = QtWidgets.QWidget()
            tab.setObjectName(f"T{level}")
            self.tab_widget.addTab(tab, f"{level + 1}")
            self.level_tabs.append(tab)
            scene = QGraphicsScene()
            self.maze.scenes.append(scene)
            tab.resize(geometry.width(), geometry.height())
            gv = QtWidgets.QGraphicsView(scene, tab)
            gv.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
            gv.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
            gv.setMinimumSize(QtCore.QSize(290, 340))
            gv.setObjectName(f"L{level}")
            self.adjust_gx(gv, scene, geometry)
            self.level_gx.append(gv)
        self.maze.reset(self.width, self.height, self.levels)
        self.maze.draw(self.demi, self.cell_size)
        for idx in range(self.levels):
            self.adjust_gx(self.level_gx[idx], self.maze.scenes[idx], geometry)
        self.tab_widget.setCurrentIndex(self.tmp_idx % self.levels)

    def depth_change(self):
        if self.level_tabs:
            idx = self.tab_widget.currentIndex()
            dt = QRect(self.level_tabs[idx].frameGeometry())
            self.levels = self.form.fields['Levels'].value()
            self.level_resize()

    def level_resize(self):
        self.tab_widget.hide()
        if self.level_tabs:
            idx = self.tab_widget.currentIndex()
            dt = QRect(self.level_tabs[idx].frameGeometry())
            self.cell_size = self.form.fields['Size'].value()
            self.width = ceil((dt.width() - self.offset) // self.cell_size)
            self.height = ceil((dt.height() - self.offset) // self.cell_size)
            self.form.fields['Width'].setText(f"{self.width}")
            self.form.fields['Height'].setText(f"{self.height}")
            self.draw_maze(dt)
        self.tab_widget.show()
        self.update()


    def adjust_gx(self, gx, scene, frame):
        # this frame is the tab container.
        gx.resize(int(frame.width()), int(frame.height()))
        # gx.mapFromScene(scene.sceneRect())
        # don't seem to need the following
        gr = gx.frameGeometry()
        sr = scene.sceneRect()
        cp = gr.center()
        sr.moveCenter(cp)
        scene.setSceneRect(sr)

    def resizeEvent(self, event):
        self.level_resize()
        super().resizeEvent(event)

    def setup(self):
        self.maze = Maze()
        self.setWindowTitle("Configure")
        self.setObjectName("Dialog")
        size_policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(size_policy)
        self.horizontal_layout = QtWidgets.QHBoxLayout(self)
        self.horizontal_layout.setObjectName("horizontal_layout")

        dt = QRect(0, 0, 304, 351)
        self.draw_maze(dt)

        self.form.widget = QtWidgets.QWidget(self)
        self.form.configure()
        self.horizontal_layout.addWidget(self.form.widget)
        self.form.fields['Size'].valueChanged.connect(self.level_resize)
        self.form.fields['Levels'].valueChanged.connect(self.depth_change)
        self.form.fields['Size'].setValue(self.cell_size)
        self.form.fields['Levels'].setValue(self.levels)


class Form(object):
    def __init__(self):
        self.form = None
        self.widget = None
        self.label_text = ('Levels', 'Size', 'Width', 'Height')
        self.minimums = (1, 16)
        self.maximums = (20, 320)
        self.labels = []
        self.fields = {}

    def configure(self):
        self.form = QtWidgets.QFormLayout(self.widget)
        self.form.setObjectName("form")
        self.widget.setMaximumSize(QtCore.QSize(160, 200))
        self.widget.setMinimumSize(QtCore.QSize(160, 200))

        # Create the fields within the form layout
        for field in range(4):
            if field < 2:
                ui = QtWidgets.QSpinBox(self.widget)
                ui.setMinimum(self.minimums[field])
                ui.setMaximum(self.maximums[field])
                ui.setMinimumSize(QtCore.QSize(60, 0))
                ui.setObjectName(f"f_{field}")
            else:
                ui = QtWidgets.QLabel(self.widget)
                ui.setObjectName(f"f_{field}")
                ui.setText(f"{0}")
            self.form.setWidget(field + 1, QtWidgets.QFormLayout.FieldRole, ui)
            self.fields[self.label_text[field]] = ui
            label = QtWidgets.QLabel(self.widget)
            label.setObjectName(f"label_{field}")
            label.setText(self.label_text[field])
            self.form.setWidget(field + 1, QtWidgets.QFormLayout.LabelRole, label)
            self.labels.append(label)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    dialog = MyDialog(Form())
    dialog.setup()
    dialog.show()
    result = app.exec_()
    pass
