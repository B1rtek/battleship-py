from enum import Enum

from PySide2.QtCore import Qt
from PySide2.QtGui import QPixmap, QIcon
from PySide2.QtWidgets import QMainWindow, QToolButton, QSizePolicy, \
    QGridLayout

from board import GameBoard, FieldStatus, translate_coordinates, Board
from fleet import Fleet, Ship


def load_icons():
    return {
        FieldStatus.NOTHING: QIcon(QPixmap("res/nothing.png")),
        FieldStatus.MISS: QIcon(QPixmap("res/miss.png")),
        FieldStatus.SHIP: QIcon(QPixmap("res/ship.png")),
        FieldStatus.SUNK: QIcon(QPixmap("res/sunk.png")),
        FieldStatus.SELECTED: QIcon(QPixmap("res/sel.png"))
    }


def translate_coords(x, y):
    alphabet = "abcdefghij"
    return alphabet[x], y + 1


# Original code by Oleh Prypin distributed under terms of the CC BY-SA 4.0
# license
# Source: https://stackoverflow.com/questions/11008140/pyqt-custom-widget-fixed-as-square
class BoardButton(QToolButton):
    def __init__(self, parent=None):
        super().__init__(parent)
        policy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        policy.setHeightForWidth(True)
        self.setSizePolicy(policy)
        self.setMaximumSize(40, 40)
        self._x = ""
        self._y = 0
        self._left_click_action = None
        self._right_click_action = None

    def heightForWidth(self, width) -> int:
        return width

    def resizeEvent(self, e):
        self.setMinimumWidth(self.height())

    def mousePressEvent(self, QMouseEvent):
        if QMouseEvent.button() == Qt.LeftButton:
            self._left_click_action(self._x, self._y)
        elif QMouseEvent.button() == Qt.RightButton:
            self._right_click_action(self._x, self._y)

    def _perform_left_click_action(self):
        self._left_click_action(self._x, self._y)

    def _perform_right_click_action(self):
        self._right_click_action(self._x, self._y)

    def set_left_click_action(self, function):
        self._left_click_action = function

    def set_right_click_action(self, function):
        self._right_click_action = function

    def set_game_coordinates(self, x: str, y: int):
        self._x = x
        self._y = y

    def get_game_coordinates(self):
        return self._x, self._y


class UIBoardMode(Enum):
    FLEET_CREATOR = 0,
    GAME = 1


class UIBoard:
    """
    Representation of GameBoard() in the UI
    """

    def __init__(self):
        """
        Initializes all values and creates a button array
        """
        self._cached_board = Board()
        self._mode = UIBoardMode.FLEET_CREATOR
        self._icons = {}
        self._button_array = []
        self._create_button_array()
        self._initialize_cached_board()

    def _create_button_array(self):
        """
        Creates the button array which will be shown in the GUI
        """
        for y in range(10):
            row = []
            for x in range(10):
                button = BoardButton()
                c_x, c_y = translate_coords(x, y)
                button.set_game_coordinates(c_x, c_y)
                row.append(button)
            self._button_array.append(row)

    def _initialize_cached_board(self):
        for c_x in "abcdefghij":
            for c_y in range(1, 11):
                self._cached_board.set_field_status(c_x, c_y, FieldStatus.SUNK)

    def set_icons(self, icons_dict: dict):
        """
        Sets the provided icons dictionary as the one used by this board
        :param icons_dict: Dictionary containing all icons needed
        :type icons_dict: dict
        """
        self._icons = icons_dict

    def update_board(self, display_board: Board, selected_ship: Ship = None):
        """
        Updates the displayed board
        :param display_board: display board from Game or FleetCreator
        :param selected_ship: Selected ship that will be marked in a special
        way on the board, only used in the FleetCreator
        """
        for c_y in range(1, 11):
            for c_x in "abcdefghij":
                new_status = display_board.get_field_status(c_x, c_y)
                if self._cached_board.get_field_status(c_x, c_y) != new_status:
                    x, y = translate_coordinates(c_x, c_y)
                    self._button_array[y][x].setIcon(self._icons[new_status])
                    self._cached_board.set_field_status(c_x, c_y, new_status)
        if selected_ship is not None:
            selected = selected_ship.get_segment_coordinates()
            for c_x, c_y in selected:
                x, y = translate_coordinates(c_x, c_y)
                self._button_array[y][x].setIcon(
                    self._icons[FieldStatus.SELECTED])
                self._cached_board.set_field_status(c_x, c_y,
                                                    FieldStatus.SELECTED)

    def define_left_click_action(self, function):
        for row in self._button_array:
            for button in row:
                button.set_left_click_action(function)

    def define_right_click_action(self, function):
        for row in self._button_array:
            for button in row:
                button.set_right_click_action(function)

    def place_button_array(self, parent_grid_layout: QGridLayout):
        for x, row in enumerate(self._button_array):
            for y, button in enumerate(row):
                parent_grid_layout.addWidget(button, x, y)


class UIFleet:
    """
    Representation of Fleet() in the UI, most likely temporary
    """

    def __init__(self, fleet: Fleet):
        self._game_board = fleet
        self._button_array = []

    def create_array(self, parent_grid_layout: QGridLayout):
        """
        Creates an array of buttons in the specified QGridLayout
        :param parent_grid_layout: QGridLayout in which the array will be
        created
        :type parent_grid_layout: QGridLayout
        """
        for y in range(2):
            row = []
            for x in range(14):
                button = BoardButton()
                row.append(button)
                parent_grid_layout.addWidget(button, y, x)
            self._button_array.append(row)
