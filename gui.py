from PySide2.QtCore import Qt
from PySide2.QtGui import QPixmap, QIcon
from PySide2.QtWidgets import QMainWindow, QToolButton, QSizePolicy

from ui_battleship import Ui_MainWindow


def load_icon():
    filename = "tile.png"
    pixmap = QPixmap(filename)
    icon = QIcon(pixmap)
    return icon


def translate_coords(x, y):
    alphabet = "abcdefghij"
    return alphabet[x], y + 1


# Original code by Oleh Prypin distributed under terms of the CC BY-SA 4.0
# license
# Source: https://stackoverflow.com/questions/11008140/pyqt-custom-widget-fixed-as-square
class SquareButton(QToolButton):
    def __init__(self, parent=None):
        super().__init__(parent)
        policy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        policy.setHeightForWidth(True)
        self.setSizePolicy(policy)
        self.setMaximumSize(40, 40)

    def heightForWidth(self, width) -> int:
        return width

    def resizeEvent(self, e):
        self.setMinimumWidth(self.height())


class BattleshipWindow(QMainWindow):
    """
    The game window class
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
