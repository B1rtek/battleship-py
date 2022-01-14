from PySide2.QtCore import Qt
from PySide2.QtGui import QPixmap, QIcon
from PySide2.QtWidgets import QToolButton, QSizePolicy, \
    QGridLayout

from board import FieldStatus, game_to_array_coords, Board
from fleet import Fleet, Ship


def load_icons():
    return {
        FieldStatus.NOTHING: QIcon(QPixmap("res/nothing.png")),
        FieldStatus.MISS: QIcon(QPixmap("res/miss.png")),
        FieldStatus.SHIP: QIcon(QPixmap("res/ship.png")),
        FieldStatus.SUNK: QIcon(QPixmap("res/sunk.png")),
        FieldStatus.SELECTED: QIcon(QPixmap("res/sel.png"))
    }


def translate_coords(x: int, y: int) -> tuple[str, int]:
    """
    Translates coordinates from array indices to game field coordinates
    :param x: x index of a field
    :type x: int
    :param y: y index of a field
    :type y: int
    :return: tuple containing field coordinates of the field on this position
    in the array
    """
    alphabet = "abcdefghij"
    return alphabet[x], y + 1


# Original code by Oleh Prypin distributed under terms of the CC BY-SA 4.0
# license
# Source: https://stackoverflow.com/questions/11008140/pyqt-custom-widget-fixed-as-square
class BoardButton(QToolButton):
    """
    Represents a single button on the board and a segment displaying a ship
    in the Fleet displays under boards on the Game screen
    """

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
        """
        Ensures that the button is (almost) always square
        """
        return width

    def resizeEvent(self, e):
        """
        Ensures that the fields don't become too small when resizing the window
        """
        self.setMinimumWidth(self.height())

    def mousePressEvent(self, QMouseEvent):
        """
        Calls functions assigned to the left and right clicks in this button
        """
        if QMouseEvent.button() == Qt.LeftButton:
            self._left_click_action(self._x, self._y)
        elif QMouseEvent.button() == Qt.RightButton:
            self._right_click_action(self._x, self._y)

    def set_left_click_action(self, function):
        """
        Sets the _left_click_action to function
        :param function: a function or a method to be set to be executed by
        this button when it's clicked on with the left mouse button
        """
        self._left_click_action = function

    def set_right_click_action(self, function):
        """
        Sets the _right_click_action to function
        :param function: a function or a method to be set to be executed by
        this button when it's clicked on with the right mouse button
        """
        self._right_click_action = function

    def set_game_coordinates(self, x: str, y: int):
        """
        Sets this button's in game coordinates
        :param x: x coordinate of a field
        :type x: str
        :param y: y coordinate of a field
        :type y: int
        """
        self._x = x
        self._y = y


class UIBoard:
    """
    Representation of GameBoard in the UI
    """

    def __init__(self):
        """
        Initializes all values and creates a button array
        """
        self._cached_board = Board()
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
        """
        Initializes the _cached_board by setting all fields' statuses to
        FieldStatus.SUNK to ensure that all of the buttons in this UIBoard will
        refresh their state and start showing the correct start state as the
        Setup phase or the Game begins, as the update_board() function only
        refreshes a button if there was a change of state of it's corresponding
        field to improve performance
        """
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
        Updates the displayed board by changing icons of the buttons which
        corresponding fields' status has changed. Only the fields with their
        status changed are updated to improve performance
        :param display_board: display board from Game or FleetCreator
        :type display_board: Board
        :param selected_ship: Selected ship that will be marked in a special
        way on the board, only used in the FleetCreator
        :type selected_ship: Ship
        """
        for c_y in range(1, 11):
            for c_x in "abcdefghij":
                new_status = display_board.get_field_status(c_x, c_y)
                if self._cached_board.get_field_status(c_x, c_y) != new_status:
                    x, y = game_to_array_coords(c_x, c_y)
                    self._button_array[y][x].setIcon(self._icons[new_status])
                    self._cached_board.set_field_status(c_x, c_y, new_status)
        if selected_ship is not None:
            selected = selected_ship.get_segment_coordinates()
            for c_x, c_y in selected:
                x, y = game_to_array_coords(c_x, c_y)
                self._button_array[y][x].setIcon(
                    self._icons[FieldStatus.SELECTED])
                self._cached_board.set_field_status(c_x, c_y,
                                                    FieldStatus.SELECTED)

    def define_left_click_action(self, function):
        """
        Sets a function or a method that will be called when a button in this
        UIBoard is clicked on with the left mouse button
        :param function: a function or a method to assign to the buttons
        """
        for row in self._button_array:
            for button in row:
                button.set_left_click_action(function)

    def define_right_click_action(self, function):
        """
        Sets a function or a method that will be called when a button in this
        UIBoard is clicked on with the right mouse button
        :param function: a function or a method to assign to the buttons
        """
        for row in self._button_array:
            for button in row:
                button.set_right_click_action(function)

    def place_button_array(self, parent_grid_layout: QGridLayout):
        """
        Creates the array in the actual window's UI
        :param parent_grid_layout: grid layout in which the board will be
        placed
        :type parent_grid_layout: QGridLayout
        """
        for x, row in enumerate(self._button_array):
            for y, button in enumerate(row):
                parent_grid_layout.addWidget(button, x, y)


class UIFleet:
    """
    Representation of Fleet() in the UI, most likely temporary
    """

    def __init__(self):
        """
        Initializes all values and creates a button array
        """
        self._cached_fleet = Fleet()
        self._icons = {}
        self._button_array = []
        self._positions_array = [
            [(0, 0), (1, 0), (2, 0), (3, 0)],
            [(5, 0), (6, 0), (7, 0)],
            [(9, 0), (10, 0), (11, 0)],
            [(0, 1), (1, 1)],
            [(3, 1), (4, 1)],
            [(12, 1), (13, 1)],
            [(6, 1)],
            [(8, 1)],
            [(10, 1)],
            [(13, 0)]
        ]
        self._create_button_array()
        self._initialize_cached_fleet()

    def _create_button_array(self):
        """
        Creates the button array which will be shown in the GUI
        """
        for ship_pos_list in self._positions_array:
            row = []
            for _ in ship_pos_list:
                button = BoardButton()
                button.set_game_coordinates("", 0)
                row.append(button)
            self._button_array.append(row)

    def _initialize_cached_fleet(self):
        """
        Initializes the _cached_fleet by setting all segments' statuses to
        FieldStatus.SUNK to ensure that all of the display buttons in this
        UIFleet will refresh their state and start showing the correct start
        state at the beginning of the game, as the update_board() function only
        refreshes a button if there was a change of state of it's corresponding
        ShipSegment to improve performance
        """
        self._cached_fleet.create_random()
        ships = self._cached_fleet.ships()
        for ship in ships:
            for segment in ship.segments():
                segment.sink()

    def set_icons(self, icons_dict: dict):
        """
        Sets the provided icons dictionary as the one used by this board
        :param icons_dict: Dictionary containing all icons needed
        :type icons_dict: dict
        """
        self._icons = icons_dict

    def update_fleet_display(self, display_fleet: Fleet):
        """
        Updates the displayed fleet by changing icons of the buttons which
        corresponding fields' status has changed. Only the fields with their
        status changed are updated to improve performance
        :param display_fleet: display fleet from Game
        :type display_fleet: Fleet
        """
        ships = display_fleet.ships()
        cached_ships = self._cached_fleet.ships()
        for ship_num, row in enumerate(self._positions_array):
            segments = ships[ship_num].segments()
            cached_segments = cached_ships[ship_num].segments()
            for segment_num, ui_segment, in enumerate(row):
                segment = segments[segment_num]
                cached_segment = cached_segments[segment_num]
                if cached_segment.sunk() != segment.sunk():
                    if segment.sunk():
                        self._button_array[ship_num][segment_num].setIcon(
                            self._icons[FieldStatus.SUNK])
                        cached_segment.sink()
                    else:
                        self._button_array[ship_num][segment_num].setIcon(
                            self._icons[FieldStatus.SHIP])
                        cached_segment.unsink()

    def define_left_click_action(self, function):
        """
        Sets a function or a method that will be called when a button in this
        UIFleet is clicked on with the left mouse button
        :param function: a function or a method to assign to the buttons
        """
        for row in self._button_array:
            for button in row:
                button.set_left_click_action(function)

    def define_right_click_action(self, function):
        """
        Sets a function or a method that will be called when a button in this
        UIFleet is clicked on with the right mouse button
        :param function: a function or a method to assign to the buttons
        """
        for row in self._button_array:
            for button in row:
                button.set_right_click_action(function)

    def place_button_array(self, parent_grid_layout: QGridLayout):
        """
        Creates the array in the actual window's UI
        :param parent_grid_layout: grid layout in which the fleet will be
        placed
        :type parent_grid_layout: QGridLayout
        """
        for positions, row in zip(self._positions_array, self._button_array):
            for position, button in zip(positions, row):
                y, x = position
                parent_grid_layout.addWidget(button, x, y)
