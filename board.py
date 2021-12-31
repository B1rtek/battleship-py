from enum import Enum

import fleet


class FieldStatus(Enum):
    NOTHING = 0,  # default status for undiscovered fields
    MISS = 1,  # set when a shot missed because there was no ship on the field
    SHIP = 2,  # indicates that a part of a ship is located on this field
    SUNK = 3  # indicates that this field contains a sunken ship


class Field:
    """
    Class that stores information about a field on a game board.
    """

    def __init__(self):
        """
        Initializes a field, assigning it a status of FieldStatus.NOTHING
        """
        self._status = FieldStatus.NOTHING

    def __str__(self) -> str:
        """
        Used to print out the fields in the console
        :return: a character representing a field's status
        """
        if self._status == FieldStatus.NOTHING:
            return ' '
        elif self._status == FieldStatus.MISS:
            return '.'
        elif self._status == FieldStatus.SHIP:
            return '█'
        else:  # FieldStatus.SUNK
            return '▒'

    def status(self) -> FieldStatus:
        return self._status

    def set_status(self, new_status: FieldStatus):
        self._status = new_status


def translate_coordinates(x: str, y: int) -> tuple[int, int]:
    """
    Function used to translate in-game coordinates (like a 7) to board field
    coordinates (a 7 is 0 6, since a is the first column and 7 is the 7th row,
    and computers count from 0).
    :param x: x coordinate of the field, a letter from a to j
    :type x: str
    :param y: y coordinate of the field, a number from 1 to 10
    :type y: int
    :return: a tuple of coordinates translated to indices of the fields array
    """
    x = x.lower()
    coord_x = ord(x) - 97
    coord_y = y - 1
    return coord_x, coord_y


class Board:
    """
    Class being an array of fields, representing a 10x10 board
    """

    def __init__(self):
        """
        Creates a 10x10 array with empty fields, which status can be set with
        set_field_status() method
        """
        self._fields = []
        for y in range(10):
            row = []
            for x in range(10):
                row.append(Field())
            self._fields.append(row)

    def __str__(self):
        """
        Prints out the contents of this board
        """
        board_str = "   abcdefghij\n\n"
        for number, row in enumerate(self._fields):
            current = f"{(number+1):>2} "
            for field in row:
                current += str(field)
            current += '\n'
            board_str += current
        return board_str

    def place_ship(self, ship: fleet.Ship):
        """
        Places a ship on the board by marking all fields it occupies with a
        status of FieldStatus.SHIP
        :param ship: Ship to be placed
        :type ship: Ship
        """
        segments = ship.segments()
        for segment in segments:
            x, y = segment.position()
            self.set_field_status(x, y, FieldStatus.SHIP)

    def place_fleet(self, fleet_to_place: fleet.Fleet):
        """
        Places ships defined in ships on the board
        :param fleet_to_place: a Fleet containing player's ships
        :type fleet_to_place: Fleet
        """
        ships = fleet_to_place.ships()
        for ship in ships:
            self.place_ship(ship)

    def get_field_status(self, x: str, y: int) -> FieldStatus:
        c_x, c_y = translate_coordinates(x, y)
        return self._fields[c_y][c_x].status()

    def set_field_status(self, x: str, y: int, status: FieldStatus):
        c_x, c_y = translate_coordinates(x, y)
        self._fields[c_y][c_x].set_status(status)


class GameBoard:
    """
    Board used in game, consists of two Boards, one of them being the data
    board, visible for the player, and one of them being the visible board,
    seen by the enemy, based on the data board.
    """

    def __init__(self, data_board: Board):
        """
        Creates a GameBoard, by taking a data board and creating a visible
        board for it
        :param data_board: raw board with all positions of the ships etc
        :type data_board: Board
        """
        self._data_board = data_board
        self._visible_board = Board()

    def discover_field(self, x: str, y: int) -> bool:
        """
        Discovers a field when a player decides to shoot at it.
        :param x: x coordinate of the field
        :type x: str
        :param y: y coordinate of the field
        :type y: int
        :return: true if there was a hit, false if it was a miss. The return
        value will be used to check which ship has been hit, and if that ship
        sunk because of it
        """
        field_status = self._data_board.get_field_status(x, y)
        self._visible_board.set_field_status(x, y, field_status)
        if field_status == FieldStatus.SHIP:
            return True
        return False

    def mark_as_empty(self, x: str, y: int):
        """
        Marks a field as empty (with a miss) on the visible board, as a visual
        indicator for a player
        :param x: x coordinate of the field
        :type x: str
        :param y: y coordinate of the field
        :type y: int
        """
        self._visible_board.set_field_status(x, y, FieldStatus.MISS)

    def print_board(self, draw_as_enemy: bool = False):
        """
        Prints the board in the given mode
        :param draw_as_enemy: if set to true, draws the version of the board
        visible to the enemy, otherwise it prints out the data board
        :type draw_as_enemy: bool
        """
        if draw_as_enemy:
            print(self._visible_board)
        else:
            print(self._data_board)
