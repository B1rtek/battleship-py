from random import choice

import board


class ShipSegment:
    """
    Class representing a part of a ship on the board
    """

    def __init__(self, x: str, y: int):
        """
        Creates a segment setting its position and status to not sunk
        :param x: x coordinate of this segment
        :type x: str
        :param y: y coordinate of this segment
        :type y: int
        """
        self._x = x
        self._y = y
        self._sunk = False

    def x(self):
        return self._x

    def y(self):
        return self._y

    def position(self):
        return self._x, self._y

    def sink(self):
        self._sunk = True

    def sunk(self):
        return self._sunk


class Ship:
    """
    Class containing information about a single ship. It contains coordinates
    of all its parts, and it can tell if it sunk or not.
    """

    def __init__(self, origin: tuple[str, int], size: int,
                 vertical: bool = True):
        """
        Creates a ship according to the given parameters:
        :param origin: The position of the upper left segment of the ship
        :type origin: tuple
        :param size: length of the ship
        :type size: int
        :param vertical: If set to true, the ship will be created vertically,
        otherwise it'll be created horizontally, by default set to True
        :type vertical: bool
        """
        self._segments = []
        x, y = origin
        if vertical:
            field_coordinates = [(x, i) for i in range(y, y + size)]
        else:
            field_coordinates = [(chr(i), y) for i in
                                 range(ord(x), ord(x) + size)]
        for x, y in field_coordinates:
            self._segments.append(ShipSegment(x, y))

    def __str__(self):
        """
        Prints out a representation of the ship's condition in a graphical form
        For example, "████" represents a ship of size 4 without any damage,
        "█XX" represents a ship of size 3 with two of its segments destroyed.
        """
        representation = ""
        for segment in self._segments:
            representation += 'X' if segment.sunk() else '█'
        return representation

    def check_if_hit(self, x: str, y: int) -> bool:
        """
        Checks if the given coordinates belong to any of this Ship's segments
        :param x: x coordinate of a field
        :type x: str
        :param y: y coordinate of a field
        :type y: int
        :return: True if the given coordinates belong to this Ship's segments,
        otherwhise False
        """
        for segment in self._segments:
            if segment.position() == (x, y):
                return True
        return False

    def sunk(self) -> bool:
        """
        Checks if this Ship sunk, checking if all of its segments sunk
        :return: True if it did, False otherwise
        """
        for segment in self._segments:
            if not segment.sunk():
                return False
        return True

    def sink(self, x: str, y: int):
        """
        Sinks the specified segment of this ship. Always called after
        check_if_hit
        :param x: x coordinate of a segment
        :type x: str
        :param y: y coordinate of a segment
        :type y: int
        """
        for segment in self._segments:
            if segment.position() == (x, y):
                segment.sink()
                return

    def segments(self):
        return self._segments


valid_x_coords = "abcdefghij"


def field_on_board(field: tuple[str, int]) -> bool:
    """
    Checks if given coordinates are a coordinates of a valid field on a board
    :param field: tuple of a field's coordinates
    :type field: tuple
    :return: True if coordinates point to a field on the board, otherwise False
    """
    x, y = field
    if x in valid_x_coords and 1 <= y <= 10:
        return True
    return False


def field_available(x, y, size, rotation, temp_board):
    """
    Checks if a ship with given position, size and rotation can be placed on
    the board, checking if all segments of the ship have valid board
    coordinates, and if it doesn't collide with any ships placed earlier
    :param x: x coordinate of the proposed Ship's origin
    :type x: str
    :param y: y coordinate of the proposed Ship's origin
    :type y: int
    :param size: size od the proposed Ship
    :type size: int
    :param rotation: rotation of the proposed Ship, True means vertical, False
    means horizontal, just like in the Ship class constructor
    :type rotation: bool
    :param temp_board: board on which the proposed Ship is to be placed
    :type temp_board: Board
    :return: True if the proposed Ship can be placed, False otherwise
    """
    temp_ship = Ship((x, y), size, rotation)
    fields = [segment.position() for segment in
              temp_ship.segments()]
    for field in fields:
        if field_on_board(field):
            f_x, f_y = field
            status = temp_board.get_field_status(f_x, f_y)
            if status != board.FieldStatus.NOTHING:
                return False
        else:
            return False
    return True


def mark_misses_around(ship: Ship, placement_board: "board.Board"):
    """
    Marks fields around the Ship with FieldStatus.MISS to prevent ships from
    generating directly next to each other. Fields that will be occupied by
    the ship are also marked, as placing the ship will change their status to
    the correct one.
    :param ship: Ship around which the fields will be marked
    :type ship: Ship
    :param placement_board: Board on which the fields will be marked
    :type placement_board: Board
    """
    segments = ship.segments()
    for segment in segments:
        s_x, s_y = segment.position()
        tl_x, tl_y = chr(ord(s_x) - 1), s_y - 1
        x_range = [chr(i) for i in range(ord(tl_x), ord(tl_x) + 3)]
        y_range = [i for i in range(tl_y, tl_y + 3)]
        for x in x_range:
            for y in y_range:
                if field_on_board((x, y)):
                    placement_board.set_field_status(x, y,
                                                     board.FieldStatus.MISS)


class Fleet:
    """
    Class containing information about a fleet of ships
    """

    def __init__(self):
        """
        Initializes a Fleet by creating an empty list of ships
        """
        self._ships = []

    def create_random(self):
        """
        Creates ships in random places on the board. Used by the computer
        enemy to place ships. First, the rotation of the ship is chosen, and
        then a list of fields where a ship can be placed is made. Then, for
        every ship, a location is chosen, and the cycle continues, until all
        ships are placed. To test if a location for a ship is valid, ships are
        placed on a temporary board.
        """
        # True means vertical, just like in the Ship class constructor
        rotations = [choice([True, False]) for _ in range(10)]
        sizes = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]
        temp_board = board.Board()
        for rotation, size in zip(rotations, sizes):
            good_coords = []
            for x in valid_x_coords:
                for c_y in range(10):
                    y = c_y + 1
                    if field_available(x, y, size, rotation, temp_board):
                        good_coords.append((x, y))
            position = choice(good_coords)
            ship_to_add = Ship(position, size, rotation)
            self._ships.append(ship_to_add)
            mark_misses_around(ship_to_add, temp_board)
            temp_board.place_ship(ship_to_add)

    def ships(self):
        return self._ships


def main():
    fleet = Fleet()
    fleet.create_random()
    game_board = board.Board()
    game_board.place_fleet(fleet)
    print(game_board)


if __name__ == "__main__":
    main()
