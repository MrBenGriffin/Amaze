from itertools import product
from math import ceil
from random import choices
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import QPen, QPainterPath
from PyQt5.QtWidgets import QGraphicsScene, QTabWidget, QDialog, QWidget, QGraphicsView
from PyQt5.QtCore import Qt, QRect, QPointF


class Art:
    normal = 100
    w_off = 2
    line = normal / 2
    t_l = QPointF(-line + w_off, -line + w_off)
    t_r = QPointF(+line - w_off, -line + w_off)
    b_r = QPointF(+line - w_off, +line - w_off)
    b_l = QPointF(-line + w_off, +line - w_off)

    @staticmethod
    def _poly(edges):
        pt = [Art.t_r, Art.b_r, Art.b_l, Art.t_l]
        path = QPainterPath()
        path.moveTo(Art.t_l)
        for i in range(4):
            path.lineTo(pt[i]) if edges[i] else path.moveTo(pt[i])
        return path

    def __init__(self):
        self.x = 1
        self.y = 1
        self.z = 1
        self.cells = {}
        self.scenes = []
        self.polygons = {x: self._poly(x) for x in product((False, True), repeat=4)}

    def reset(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        self.cells = {tuple((ix, iy, iz)): tuple(choices([True, False], k=4))
                      for ix in range(self.x)
                      for iy in range(self.y)
                      for iz in range(self.z)
                      }
        for scene in self.scenes:
            scene.clear()

    def draw(self):
        pen = QPen(Qt.black, 2, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)
        for x, y, z in self.cells:
            cx1 = x * Art.normal
            cy1 = y * Art.normal
            shape = self.polygons[self.cells[x, y, z]]
            self.scenes[z].addPath(shape.translated(QPointF(cx1, cy1)), pen)


class MyDialog(QDialog):
    """
    Is the main application window, which is made of two parts:
    One one side is the pane of tabs which display the maze
    On the other are the configurable values of the maze (levels)
    """
    def __init__(self):
        self.pane = None
        self.form = None
        self.horizontal_layout = None
        super().__init__()

    def resizeEvent(self, event):
        self.pane.resize()
        super().resizeEvent(event)

    def setup(self):
        self.pane = Pane(self)
        self.form = Form(self)
        self.setWindowTitle("Configure")
        self.setObjectName("Dialog")
        size_policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(size_policy)
        self.horizontal_layout = QtWidgets.QHBoxLayout(self)
        self.horizontal_layout.setObjectName("horizontal_layout")
        self.pane.setup(self.horizontal_layout)
        self.form.setup(self.horizontal_layout)
        self.pane.connect_form(self.form)


class Pane:
    def __init__(self, parent):
        self.parent = parent    # This is the widget.
        self.layout = None      # This is the parent's layout.
        self.form = None        # This is the form used to control things.
        self.tab_group = None  # This is the tab widget, which can be fully replaced.
        # Everything below are default values.
        self.offset = 12
        self.demi = self.offset // 2
        self.loop_idx = 0
        self.levels = 4
        self.width = 0
        self.height = 0
        self.cell_size = 100
        self.art = None

    def setup(self, parent_layout):
        self.layout = parent_layout
        self.art = Art()
        self.tab_group = TabGroup(self.parent, self.layout, self.art)
        self.set_tab_widget()

    def connect_form(self, form):
        self.form = form
        self.form.set_values({'Size': self.cell_size, 'Levels': self.levels})
        self.form.set_listen({'Size': self.resize, 'Levels': self.re_depth})

    def set_tab_widget(self):
        self.tab_group.reset()  # initialises / replaces a QTabWidget into the horizontal_layout
        for level in range(self.levels):
            tab = self.tab_group.add(level)

        self.art.reset(self.width, self.height, self.levels)
        self.art.draw()
        self.loop_idx = self.tab_group.tmp_idx % self.levels
        # QtCore.QTimer.singleShot(0, self.adjust_gx)
        self.tab_group.setCurrentIndex(self.loop_idx)

    def resize(self, always=False):
        if self.tab_group:
            dim = self.tab_group.update_dim()
            self.cell_size = self.form.get_value('Size')
            new_width = ceil((dim.width() - self.offset) // self.cell_size)
            new_height = ceil((dim.height() - self.offset) // self.cell_size)
            self.tab_group.hide()
            if (new_width != self.width) or (new_height != self.height) or always:
                self.width = new_width
                self.height = new_height
                self.form.set_texts({'Width': f"{self.width}", 'Height': f"{self.height}"})
                self.set_tab_widget()
            self.tab_group.show()
            self.parent.update()

    def re_depth(self):
        self.levels = self.form.get_value('Levels')
        self.resize(True)


class TabItem(QWidget):
    def __init__(self, parent, idx, scene):
        self.parent = parent
        self.idx = idx
        self.name = f"{idx+1}"
        self.scene = scene
        self.view = None
        super().__init__()

        # View should probably be sub-classed also...
        self.view = QGraphicsView(scene, self)
        self.view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.view.setMinimumSize(QtCore.QSize(340, 340))
        self.view.setObjectName(f"view_{idx+1}")
        self.setObjectName(f"tab_{idx+1}")

    def showEvent(self, show_event=None):
        self.view.resize(self.parent.dim.width(), self.parent.dim.height())
        boundary = self.scene.itemsBoundingRect()
        self.view.fitInView(boundary, Qt.KeepAspectRatio)
        self.scene.setSceneRect(boundary)
        if show_event:
            super().showEvent(show_event)

    def close(self):
        if self.view:
            self.view.close()
        if self.scene:
            self.scene.clear()
        super().close()


class TabGroup(QTabWidget):
    def __init__(self, parent, layout, art):
        self.dim = QRect(0, 0, 360, 380)  # This is the size of the initial tab_widget
        self.tmp_idx = 0
        self.layout = layout
        self.art = art
        self.tabs = []
        super().__init__(parent)
        self.setMinimumSize(QtCore.QSize(360, 380))
        self.setTabPosition(QTabWidget.North)
        self.layout.addWidget(self)

    def reset(self):
        self.dim = self.update_dim()
        self.tmp_idx = self.currentIndex()
        for tab in self.tabs:
            tab.close()
        self.tabs = []
        self.clear()
        self.art.scenes = []
        # super().close()

    def add(self, idx):
        scene = QGraphicsScene()
        tab = TabItem(self, idx, scene)
        self.addTab(tab, tab.name)
        tab.resize(self.dim.width(), self.dim.height())
        if len(self.tabs) > idx:
            self.tabs[idx] = tab
            self.art.scenes[idx] = scene
        else:
            self.tabs.append(tab)
            self.art.scenes.append(scene)

    def update_dim(self):
        if self.tabs:
            idx = self.currentIndex()
            self.dim = QRect(self.tabs[idx].frameGeometry())
        return self.dim


class Form(QtWidgets.QWidget):
    def __init__(self, parent):
        self.parent = parent
        self.form = None
        self.label_text = ('Levels', 'Size', 'Width', 'Height')
        self.minimums = (1, 16)
        self.maximums = (20, 320)
        self.labels = []
        self.fields = {}
        super().__init__(self.parent)

    def setup(self, parent_layout):
        self.form = QtWidgets.QFormLayout(self)
        self.form.setObjectName("form")
        self.setMaximumSize(QtCore.QSize(160, 200))
        self.setMinimumSize(QtCore.QSize(160, 200))

        # Create the fields within the form layout
        for field in range(4):
            if field < 2:
                ui = QtWidgets.QSpinBox(self)
                ui.setMinimum(self.minimums[field])
                ui.setMaximum(self.maximums[field])
                ui.setMinimumSize(QtCore.QSize(60, 0))
                ui.setObjectName(f"f_{field}")
            else:
                ui = QtWidgets.QLabel(self)
                ui.setObjectName(f"f_{field}")
                ui.setText(f"{0}")
            self.form.setWidget(field + 1, QtWidgets.QFormLayout.FieldRole, ui)
            self.fields[self.label_text[field]] = ui
            label = QtWidgets.QLabel(self)
            label.setObjectName(f"label_{field}")
            label.setText(self.label_text[field])
            self.form.setWidget(field + 1, QtWidgets.QFormLayout.LabelRole, label)
            self.labels.append(label)
        parent_layout.addWidget(self)

    def get_value(self, name):
        return self.fields[name].value()

    def set_values(self, config):
        for k in config.keys():
            self.fields[k].setValue(config[k])

    def set_texts(self, config):
        for k in config.keys():
            self.fields[k].setText(config[k])

    def set_listen(self, config):
        for k in config.keys():
            self.fields[k].valueChanged.connect(config[k])


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    dialog = MyDialog()
    dialog.setup()
    dialog.show()
    result = app.exec_()
