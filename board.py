from enum import Enum

import fleet


class FieldStatus(Enum):
    NOTHING = 0,  # default status for undiscovered fields
    MISS = 1,  # set when a shot missed because there was no ship on the field
    SHIP = 2,  # indicates that a part of a ship is located on this field
    SUNK = 3,  # indicates that this field contains a sunken ship
    SELECTED = 4  # a special state used in the GUI


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
        elif self._status == FieldStatus.SUNK:
            return '▒'
        else:  # FieldStatus.SELECTED
            return '#'

    def status(self) -> FieldStatus:
        return self._status

    def set_status(self, new_status: FieldStatus):
        self._status = new_status


class InvalidGameCoordinatesError(Exception):
    """
    Raised when provided game coordinates result in invalid
    array coordinates after translation
    """

    def __init__(self, x: str, y: int):
        self.x = x
        self.y = y
        super().__init__(f"Invalid game coordinates specified: {x}, {y}")


def game_to_array_coords(x: str, y: int) -> tuple[int, int]:
    """
    Function used to translate in-game coordinates (like 'a', 7) to board field
    coordinates ('a' 7 is 0 6, since 'a' is the first column and 7 is the 7th
    row, and computers count from 0)
    :param x: x coordinate of the field, a letter from a to j
    :type x: str
    :param y: y coordinate of the field, a number from 1 to 10
    :type y: int
    :return: a tuple of coordinates translated to indices of the fields array
    """
    x = x.lower()
    coord_x = ord(x) - 97
    coord_y = y - 1
    if (not 0 <= coord_x <= 9) or (not 0 <= coord_y <= 9):
        raise InvalidGameCoordinatesError(x, y)
    return coord_x, coord_y


def return_all_field_coordinates():
    """
    Returns a list of tuples containing coordinates of all fields on the board
    :return: a list of 100 tuples with field coordinates
    """
    all_fields = []
    for x in "abcdefghij":
        for y in range(1, 11):
            all_fields.append((x, y))
    return all_fields


def field_on_board(field: tuple[str, int]) -> bool:
    """
    Checks if given coordinates are a coordinates of a valid field on a board
    :param field: tuple of a field's coordinates
    :type field: tuple
    :return: True if coordinates point to a field on the board, otherwise False
    """
    return field in return_all_field_coordinates()


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
        board_str = "   abcdefghij\n" \
                    "  +=-=-=-=-=-+\n"
        for number, row in enumerate(self._fields):
            current = f"{(number + 1):>2}"
            border = '|' if number % 2 == 0 else chr(186)
            current += border
            for field in row:
                current += str(field)
            current += border
            current += '\n'
            board_str += current
        board_str += "  +=-=-=-=-=-+"
        return board_str

    def clear_board(self):
        """
        Sets states of all fields in the board to FieldStatus.NOTHING
        """
        for y in range(10):
            for x in range(10):
                self._fields[y][x].set_status(FieldStatus.NOTHING)

    def place_ship(self, ship: "fleet.Ship"):
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

    def place_fleet(self, fleet_to_place: "fleet.Fleet"):
        """
        Places ships defined in ships on the board
        :param fleet_to_place: a Fleet containing player's ships
        :type fleet_to_place: Fleet
        """
        self.clear_board()
        for row in self._fields:
            for field in row:
                field.set_status(FieldStatus.NOTHING)
        ships = fleet_to_place.ships()
        for ship in ships:
            self.place_ship(ship)

    def mark_sunken_ship(self, ship_to_sink: "fleet.Ship"):
        """
        Marks a given ship as a sunken ship on the board
        :param ship_to_sink: Ship to be marked as sunken
        :type ship_to_sink: Ship
        """
        segments = ship_to_sink.segments()
        for segment in segments:
            x, y = segment.position()
            self.set_field_status(x, y, FieldStatus.SUNK)

    def get_field_status(self, x: str, y: int) -> FieldStatus:
        """
        Returns the status of a field on the specified coordinates
        :param x: x coordinate of a field
        :type x: str
        :param y: y coordinate of a field
        :type y: int
        :return: status of the specified field
        """
        c_x, c_y = game_to_array_coords(x, y)
        return self._fields[c_y][c_x].status()

    def set_field_status(self, x: str, y: int, status: FieldStatus):
        """
        Sets the status of a field on the specified coordinates
        :param x: x coordinate of a field
        :type x: str
        :param y: y coordinate of a field
        :type y: int
        :param status: new status of a field
        :type status: FieldStatus
        """
        c_x, c_y = game_to_array_coords(x, y)
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
        :param data_board: raw board with all positions of the ships etc.
        :type data_board: Board
        """
        self._data_board = data_board
        self._visible_board = Board()

    def discover_field(self, x: str, y: int) -> bool:
        """
        Discovers a field when a player decides to shoot at it
        :param x: x coordinate of the field
        :type x: str
        :param y: y coordinate of the field
        :type y: int
        :return: true if there was a hit, false if it was a miss. The return
        value will be used to check which ship has been hit, and if that ship
        sunk because of it
        """
        field_status = self._data_board.get_field_status(x, y)
        if field_status == FieldStatus.NOTHING:
            field_status = FieldStatus.MISS
            self._data_board.set_field_status(x, y, field_status)
        self._visible_board.set_field_status(x, y, field_status)
        if field_status == FieldStatus.SHIP:
            field_status = FieldStatus.SUNK
            self._data_board.set_field_status(x, y, field_status)
            return True
        return False

    def mark_as_empty(self, x: str, y: int) -> bool:
        """
        Marks a field as empty (with a miss) on the visible board, as a visual
        indicator for a player, only if the field that is being marked has
        nothing on it
        :param x: x coordinate of the field
        :type x: str
        :param y: y coordinate of the field
        :type y: int
        :return: True if the field was marked, False if it wasn't due to it
        containing a ship
        """
        current_status = self._visible_board.get_field_status(x, y)
        if current_status != FieldStatus.NOTHING:
            return False
        self._visible_board.set_field_status(x, y, FieldStatus.MISS)
        return True

    def unmark_as_empty(self, x: str, y: int) -> bool:
        """
        Removes the marker from the specified field
        :param x: x coordinate of the field
        :type x: str
        :param y: y coordinate of the field
        :type y: int
        :return: True if the field was marked, False if it wasn't due to it
        containing a ship
        """
        current_status = self._visible_board.get_field_status(x, y)
        if current_status != FieldStatus.MISS:
            return False
        self._visible_board.set_field_status(x, y, FieldStatus.NOTHING)
        return True

    def sink_ship(self, ship_to_sink: "fleet.Ship"):
        """
        Called when a ship in a fleet has sunk to mark him as sunk on the map
        :param ship_to_sink: Ship to be sunk
        :type ship_to_sink: Ship
        """
        self._data_board.mark_sunken_ship(ship_to_sink)
        self._visible_board.mark_sunken_ship(ship_to_sink)

    def get_display_board(self, display_as_enemy: bool = False) -> Board:
        """
        Creates a data board representing what the specified player would see
        :param display_as_enemy: if set to True, the data will reflect what the
        enemy would see, otherwise it'll look like what the player should see
        :type display_as_enemy: bool
        :return: a Board containing data necessary to draw this board on the
        screen
        """
        if display_as_enemy:
            return self._visible_board
        else:
            display_board = Board()
            for x, y in return_all_field_coordinates():
                status = self._data_board.get_field_status(x, y)
                if status == FieldStatus.NOTHING:
                    status = self._visible_board.get_field_status(x, y)
                display_board.set_field_status(x, y, status)
            return display_board

    def field_undiscovered(self, x, y) -> bool:
        """
        Checks if a field on the specified coordinates is undiscovered
        :param x: x coordinate of the field
        :type x: str
        :param y: y coordinate of the field
        :type y: int
        :return: True if the specified field is undiscovered, False otherwise
        """
        return self._visible_board.get_field_status(x,
                                                    y) == FieldStatus.NOTHING

    def mark_misses_around(self, ship_to_mark_around: "fleet.Ship"):
        fleet.mark_misses_around(ship_to_mark_around, self._visible_board)
        self.sink_ship(ship_to_mark_around)
