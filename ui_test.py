import sys
from functools import partial

from PySide2.QtCore import QSize, Qt
from PySide2.QtGui import QPixmap, QIcon
from PySide2.QtWidgets import QMainWindow, QPushButton, QHBoxLayout, \
    QApplication, QSizePolicy, QToolButton

from board import Board, GameBoard
from fleet import Fleet
from gui import UIFleet, UIBoard
from ui_battleship import Ui_Battleship


# Original code by Oleh Prypin distributed under terms of the CC BY-SA 4.0
# license
# Source: https://stackoverflow.com/questions/11008140/pyqt-custom-widget-fixed-as-square
class SquareButton(QToolButton):
    def __init__(self, parent=None):
        super().__init__(parent)
        policy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
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


def load_icons():
    return [QIcon(QPixmap("res/nothing.png")), QIcon(QPixmap("res/miss.png")),
            QIcon(QPixmap("res/ship.png")), QIcon(QPixmap("res/sunk.png"))]


def new_fleet(board: Board, ui_board: UIBoard):
    fleet = Fleet()
    fleet.create_random()
    board.place_fleet(fleet)
    ui_board.update_array()


def main(args):
    app = QApplication(args)
    window = QMainWindow()
    ui = Ui_Battleship()
    ui.setupUi(window)
    fleet = Fleet()
    fleet.create_random()
    test_board = Board()
    test_board.place_fleet(fleet)
    test_gboard = GameBoard(test_board)
    icons = load_icons()
    ui_board = UIBoard(test_gboard, icons)
    ui_board.create_array(ui.grid_setup_board)
    ui_board.create_array(ui.grid_game_player_board)
    ui_board.create_array(ui.grid_game_enemy_board)
    ui_board.update_array()
    ui_fleet = UIFleet(fleet)
    ui_fleet.create_array(ui.grid_game_player_fleet)
    ui_fleet.create_array(ui.grid_game_enemy_fleet)
    ui.button_setup_rand.clicked.connect(
        partial(new_fleet, test_board, ui_board))
    ui.button_setup_exit.clicked.connect(
        partial(ui.stackedWidget.setCurrentIndex, 0))
    ui.button_main_play.clicked.connect(
        partial(ui.stackedWidget.setCurrentIndex, 1))
    ui.button_main_htp.clicked.connect(
        partial(ui.stackedWidget.setCurrentIndex, 3))
    ui.button_htp_back.clicked.connect(
        partial(ui.stackedWidget.setCurrentIndex, 0))
    ui.button_main_quit.clicked.connect(
        partial(sys.exit, 0))
    ui.button_setup_done.clicked.connect(
        partial(ui.stackedWidget.setCurrentIndex, 2))
    ui.button_game_main.clicked.connect(
        partial(ui.stackedWidget.setCurrentIndex, 0))
    window.resize(QSize(700, 540))
    window.show()
    return app.exec_()


if __name__ == "__main__":
    main(sys.argv)
