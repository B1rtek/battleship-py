from copy import deepcopy
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
        self._size = size
        self._vertical = vertical
        self._origin = origin
        x, y = origin
        if vertical:
            field_coordinates = [(x, i) for i in range(y, y + size)]
        else:
            field_coordinates = [(chr(i), y) for i in
                                 range(ord(x), ord(x) + size)]
        for x, y in field_coordinates:
            self._segments.append(ShipSegment(x, y))

    def __str__(self, draw_as_enemy: bool = False):
        """
        Prints out a representation of the ship's condition in a graphical form
        For example, "████" represents a ship of size 4 without any damage,
        "█▒▒" represents a ship of size 3 with two of its segments destroyed.
        :param draw_as_enemy: if set to True, the ship will be drawn as a sunk
        one or undamaged one, to not indicate which ship has been struck to the
        enemy, False by default
        :type draw_as_enemy: bool
        """
        if draw_as_enemy:
            if self.sunk():
                return self._size * '▒'
            else:
                return self._size * '█'
        representation = ""
        for segment in self._segments:
            representation += '▒' if segment.sunk() else '█'
        return representation

    def check_if_belongs(self, x: str, y: int) -> bool:
        """
        Checks if the given coordinates belong to any of this Ship's segments
        :param x: x coordinate of a field
        :type x: str
        :param y: y coordinate of a field
        :type y: int
        :return: True if the given coordinates belong to this Ship's segments,
        otherwise False
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
        check_if_belongs
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

    def size(self):
        return self._size

    def vertical(self):
        return self._vertical

    def origin(self):
        return self._origin


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


def field_available(temp_ship, temp_board):
    """
    Checks if a ship with given position, size and rotation can be placed on
    the board, checking if all segments of the ship have valid board
    coordinates, and if it doesn't collide with any ships placed earlier
    :param temp_ship: a ship which placement will be tested
    :type temp_ship: Ship
    :param temp_board: board on which the proposed Ship is to be placed
    :type temp_board: Board
    :return: True if the proposed Ship can be placed, False otherwise
    """
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
        Initializes a Fleet by creating an empty list of ships. Ships in the
        self._ships list are always put in the order from biggest to smallest,
        and that's how they are generated in create_random() and create_fleet()
        methods. self._selected_ship is the ship that will be moved or rotated
        while modifying the board
        """
        self._ships = []
        self._selected_ship = None

    def __str__(self):
        """
        Returns a string containing all ships in the fleet and their current
        states. For example:
        █▒▒█ ███ ███ ▒

        ██ ██ ██ ▒ █ █
        represents a fleet with it's 4 segment ship with its middle segments
        damaged, and the first and fourth small ships destroyed.
        :return: a string representing a fleet, similar to the example shown
        above
        """
        fleet = ""
        row1 = self._ships[:3]
        row1.append(self._ships[-1])
        row2 = self._ships[3:-1]
        for ship in row1:
            fleet += str(ship) + ' '
        fleet += '\n'
        for ship in row2:
            fleet += str(ship) + ' '
        return fleet

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
                    temp_ship = Ship((x, y), size, rotation)
                    if field_available(temp_ship, temp_board):
                        good_coords.append((x, y))
            position = choice(good_coords)
            ship_to_add = Ship(position, size, rotation)
            self._ships.append(ship_to_add)
            mark_misses_around(ship_to_add, temp_board)
            temp_board.place_ship(ship_to_add)

    def create_fleet(self):
        """
        Lets a player create their own fleet by letting them choose positions
        of their ships manually.
        """
        pass

    def hit(self, x: str, y: int):
        """
        Damages a ship in the specified coordinates
        :param x: x coordinate of the field
        :type x: str
        :param y: y coordinate of the field
        :type y: int
        """
        ship_hit = self.find_ship(x, y)
        ship_hit.sink(x, y)
        pass

    def find_ship(self, x: str, y: int):
        """
        Finds a ship positioned on the selected coordinates
        :param x: x coordinate of the field
        :type x: str
        :param y: y coordinate of the field
        :type y: int
        :return: Ship situated in this position or None if there is no ship
        there
        """
        for ship in self._ships:
            if ship.check_if_belongs(x, y):
                return ship
        return None

    def select_ship(self, x: str, y: int) -> str:
        """
        Selects a ship that can be moved or rotated while setting up the fleet
        :param x: x coordinate of the field
        :type x: str
        :param y: y coordinate of the field
        :type y: int
        :return: A message stating that a ship has been selected or that it
        wasn't
        """
        self._selected_ship = self.find_ship(x, y)
        if self._selected_ship is not None:
            return "A ship has been selected"
        return "No ship was found on these coordinates"

    def set_ship_position(self, x: str, y: int) -> str:
        """
        Sets selected ship's position to the specified coordinates. Coordinates
        point to the ship's new origin. Before moving the ship, a test is
        conducted to see if the new position is valid and doesn't collide with
        any ships from this fleet.
        :param x: x coordinate of the new position
        :type x: str
        :param y: y coordinate of the new position
        :type y: int
        :return: A message stating either success or failure of the move
        """
        if self._selected_ship is None:
            return "No ship has been selected"
        vertical = self._selected_ship.vertical()
        size = self._selected_ship.size()
        new_ship = Ship((x, y), size, vertical)
        new_fleet = deepcopy(self._ships)
        old_ship_index = self._ships.index(self._selected_ship)
        new_fleet[old_ship_index] = new_ship
        # Now a test fit will be conducted to see if the fleet doesn't collide
        # with itself, and if it doesn't, the selected_ship will be assigned
        # with a reference to the new_ship, replacing it in selection and in
        # the fleet
        temp_board = board.Board()
        for ship in new_fleet:
            if field_available(ship, temp_board):
                mark_misses_around(ship, temp_board)
                temp_board.place_ship(ship)
            else:
                return "The new placement is invalid"
        # If all ships have been placed it means that a new location is good
        self._ships[old_ship_index] = new_ship
        self._selected_ship = new_ship
        return "Ship has been moved to a new location"

    def ships(self):
        return self._ships

    def is_alive(self):
        """
        Checks if the whole fleet has sunk
        :return: True if there are still ships afloat, False otherwise
        """
        for ship in self._ships:
            if not ship.sunk():
                return True
        return False


def main():
    fleet = Fleet()
    fleet.create_random()
    game_board = board.Board()
    while True:
        game_board.place_fleet(fleet)
        print(game_board)
        print(fleet)
        command, x, s_y = input("> ").split()
        y = int(s_y)
        if command == "sel":
            print(fleet.select_ship(x, y))
        elif command == "mv":
            print(fleet.set_ship_position(x, y))
        else:
            print("Unknown command")


if __name__ == "__main__":
    main()
