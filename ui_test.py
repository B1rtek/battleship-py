import sys
from functools import partial

from PySide2.QtCore import QSize, Qt
from PySide2.QtGui import QPixmap, QIcon
from PySide2.QtWidgets import QMainWindow, QPushButton, QHBoxLayout, \
    QApplication, QSizePolicy, QToolButton

from ui_battleship import Ui_MainWindow


# Original code by Oleh Prypin distributed under terms of the CC BY-SA 4.0
# license
# Source: https://stackoverflow.com/questions/11008140/pyqt-custom-widget-fixed-as-square
class SquareButton(QToolButton):
    def __init__(self, parent=None):
        super().__init__(parent)
        policy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        policy.setHeightForWidth(True)
        self.setSizePolicy(policy)
        self.x_coord = "0"
        self.y_coord = 0

    def heightForWidth(self, width) -> int:
        return width

    def resizeEvent(self, e):
        self.setMinimumWidth(self.height())

    def mousePressEvent(self, QMouseEvent):
        if QMouseEvent.button() == Qt.LeftButton:
            logger(self.x_coord, self.y_coord, "shoot")
        elif QMouseEvent.button() == Qt.RightButton:
            logger(self.x_coord, self.y_coord, "mark as empty")


def logger(x, y, mode):
    print(f"{mode}: {x} {y}")


def translate_coords(x, y):
    alphabet = "abcdefghij"
    return alphabet[x], y + 1


def load_icon():
    filename = "tile.png"
    pixmap = QPixmap(filename)
    icon = QIcon(pixmap)
    return icon


def main(args):
    app = QApplication(args)
    window = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(window)
    icon = load_icon()
    ui.containter.setHorizontalSpacing(0)
    ui.containter.setVerticalSpacing(0)
    for x in range(10):
        for y in range(10):
            button = SquareButton()
            c_x, c_y = translate_coords(x, y)
            button.x_coord = c_x
            button.y_coord = c_y
            button.setIcon(icon)
            button.setIconSize(QSize(40, 40))
            button.setAutoRaise(True)
            button.setContentsMargins(0, 0, 0, 0)
            button.setStyleSheet(
                "SquareButton::hover\n{\nbackground-color : lightgray;\n}")
            ui.containter.addWidget(button, x, y)
    window.show()
    return app.exec_()


if __name__ == "__main__":
    main(sys.argv)
