from copy import deepcopy
from random import choice
from typing import List

import board
import enemy


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

    def position(self) -> tuple[str, int]:
        """
        Returns a tuple representing this segment's position
        """
        return self._x, self._y

    def sink(self):
        """
        Sinks this segment by setting it's _sunk value to True
        """
        self._sunk = True

    def unsink(self):
        """
        "Unsinks" this segment by setting it's _sunk value to False, used to
        initialize the Fleet displays in the UI version, since they only
        refresh when there is a change in the state of the fleet, so to begin
        the game all ships must be sunk for the displays to update
        """
        self._sunk = False

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

    def get_segment_coordinates(self) -> List[tuple]:
        """
        Returns coordinates of segments that make this ship
        :return: a list tuples with segment coordinates
        """
        segments = []
        for segment in self._segments:
            segments.append(segment.position())
        return segments

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

    def sunk(self) -> bool:
        """
        Checks if this Ship sunk, checking if all of its segments sunk
        :return: True if it did, False otherwise
        """
        for segment in self._segments:
            if not segment.sunk():
                return False
        return True

    def ship_to_str(self, draw_as_enemy: bool = False) -> str:
        """
        Prints out a representation of the ship's condition in a graphical form
        For example, "████" represents a ship of size 4 without any damage,
        "█▒▒" represents a ship of size 3 with two of its segments destroyed.
        :param draw_as_enemy: if set to True, the ship will be drawn as a sunk
        one or undamaged one, to not indicate which part has been struck to the
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

    def segments(self) -> List[ShipSegment]:
        return self._segments

    def size(self) -> int:
        return self._size

    def vertical(self) -> bool:
        return self._vertical

    def origin(self) -> tuple[str, int]:
        return self._origin


def field_available(temp_ship, temp_board) -> bool:
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
    fields = temp_ship.get_segment_coordinates()
    for field in fields:
        if board.field_on_board(field):
            f_x, f_y = field
            status = temp_board.get_field_status(f_x, f_y)
            if status != board.FieldStatus.NOTHING:
                return False
        else:
            return False
    return True


def fields_around_field(source: tuple[str, int]) -> List[tuple]:
    """
    Creates a list of fields around the specified field
    :param source: the field to generate surrounding fields of
    :type source: tuple
    :return: list containing coordinates of all fields around the source field
    """
    return enemy.create_list_of_adherent(
        source) + enemy.create_list_of_tangents(source)


def fields_around_ship(ship: Ship) -> List[tuple]:
    """
    Creates a list of fields around the given ship
    :param ship: ship based on which the list will be generated
    :type ship: Ship
    :return: a list of field coordinates around that ship
    """
    all_fields = board.return_all_field_coordinates()
    ship_fields = ship.get_segment_coordinates()
    around = []
    for ship_field in ship_fields:
        fields_around_current = fields_around_field(ship_field)
        for field in fields_around_current:
            if field in all_fields and field not in around \
                    and field not in ship_fields:
                around.append(field)
    return around


def mark_misses_around(ship: Ship, placement_board: "board.Board"):
    """
    Marks fields around the Ship with FieldStatus.MISS to prevent ships from
    generating directly next to each other.
    :param ship: Ship around which the fields will be marked
    :type ship: Ship
    :param placement_board: Board on which the fields will be marked
    :type placement_board: Board
    """
    fields_around = fields_around_ship(ship)
    for x, y in fields_around:
        placement_board.set_field_status(x, y, board.FieldStatus.MISS)


class Fleet:
    """
    Class containing information about a fleet of ships
    """

    def __init__(self, ships: List[Ship] = None):
        """
        Initializes a Fleet by creating an empty list of ships. Ships in the
        self._ships list are always put in the order from biggest to smallest,
        and that's how they are generated in create_random() and create_fleet()
        methods. self._selected_ship is the ship that will be moved or rotated
        while modifying the board
        :param ships: A list of ships to initialize this fleet with
        :type ships: list
        """
        self._ships = []
        if ships is not None:
            self._ships = ships
        self._selected_ship = None

    def create_random(self):
        """
        Creates ships in random places on the board. Used by the computer
        enemy to place ships. First, the rotation of the ship is chosen, and
        then a list of fields where a ship can be placed is made. Then, for
        every ship, a location is chosen, and the cycle continues, until all
        ships are placed. To test if a location for a ship is valid, ships are
        placed on a temporary board.
        """
        self._ships.clear()
        self._selected_ship = None
        # True means vertical, just like in the Ship class constructor
        rotations = [choice([True, False]) for _ in range(10)]
        sizes = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]
        temp_board = board.Board()
        for rotation, size in zip(rotations, sizes):
            good_coords = []
            for x, y in board.return_all_field_coordinates():
                temp_ship = Ship((x, y), size, rotation)
                if field_available(temp_ship, temp_board):
                    good_coords.append((x, y))
            position = choice(good_coords)
            ship_to_add = Ship(position, size, rotation)
            self._ships.append(ship_to_add)
            mark_misses_around(ship_to_add, temp_board)
            temp_board.place_ship(ship_to_add)

    def hit(self, x: str, y: int) -> bool:
        """
        Damages a ship in the specified coordinates
        :param x: x coordinate of the field
        :type x: str
        :param y: y coordinate of the field
        :type y: int
        :return: True if the ship sinks completely, otherwise False
        """
        ship_hit = self.find_ship(x, y)
        if ship_hit is None:
            return False
        ship_hit.sink(x, y)
        if ship_hit.sunk():
            return True
        return False

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

    def select_ship(self, x: str, y: int) -> bool:
        """
        Selects a ship that can be moved or rotated while setting up the fleet
        :param x: x coordinate of the field
        :type x: str
        :param y: y coordinate of the field
        :type y: int
        :return: True if ship was selected, False otherwise
        """
        self._selected_ship = self.find_ship(x, y)
        if self._selected_ship is not None:
            return True
        return False

    def _new_ship_test_fit(self, new_ship: Ship) -> int:
        """
        Checks if the fleet with a new ship instead of the selected one doesn't
        collide with itself. This method is only used by set_ship_position
        and change_ship_rotation methods
        :param new_ship: a new ship that this fleet will be tested with
        :type new_ship: Ship
        :return: new_ship's index in the self._ships list if it fits with the
        other ships, otherwise -1 to indicate that it can't be placed
        """
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
                return -1
        # If all ships have been placed it means that a new location is good
        return old_ship_index

    def set_ship_position(self, x: str, y: int) -> bool:
        """
        Sets selected ship's position to the specified coordinates. Coordinates
        point to the ship's new origin. Before moving the ship, a test is
        conducted to see if the new position is valid and doesn't collide with
        any ships from this fleet.
        :param x: x coordinate of the new position
        :type x: str
        :param y: y coordinate of the new position
        :type y: int
        :return: True if moving the ship to a new position was successful,
        False otherwise
        """
        if self._selected_ship is None:
            return False
        vertical = self._selected_ship.vertical()
        size = self._selected_ship.size()
        new_ship = Ship((x, y), size, vertical)
        old_ship_index = self._new_ship_test_fit(new_ship)
        if old_ship_index == -1:
            return False
        self._ships[old_ship_index] = new_ship
        self._selected_ship = new_ship
        return True

    def change_ship_rotation(self) -> bool:
        """
        Changes selected ship's rotation from vertical to horizontal, or the
        other way, rotating it around its origin. Just like in
        set_ship_position, a test fit is conducted to see if the rotated ship
        doesn't collide with any other ships.
        :return: True if rotation was successful, False otherwise
        """
        if self._selected_ship is None:
            return False
        vertical = not self._selected_ship.vertical()
        size = self._selected_ship.size()
        x, y = self._selected_ship.origin()
        new_ship = Ship((x, y), size, vertical)
        old_ship_index = self._new_ship_test_fit(new_ship)
        if old_ship_index == -1:
            return False
        self._ships[old_ship_index] = new_ship
        self._selected_ship = new_ship
        return True

    def is_alive(self):
        """
        Checks if the whole fleet has sunk
        :return: True if there are still ships afloat, False otherwise
        """
        for ship in self._ships:
            if not ship.sunk():
                return True
        return False

    def fleet_to_str(self, draw_as_enemy: bool = False) -> str:
        """
        Returns a string containing all ships in the fleet and their current
        states. For example:
        █▒▒█ ███ ███ ▒
        ██ ██ ██ ▒ █ █
        represents a fleet with it's 4 segment ship with its middle segments
        damaged, and the first and fourth small ships destroyed.
        :param draw_as_enemy: if set to True, the ships will be drawn as a sunk
        or undamaged, to not indicate which ship has been struck to the
        enemy, False by default
        :type draw_as_enemy: bool
        :return: a string representing a fleet, similar to the example shown
        above
        """
        fleet = ""
        row1 = self._ships[:3]
        row1.append(self._ships[-1])
        row2 = self._ships[3:-1]
        for ship in row1:
            fleet += ship.ship_to_str(draw_as_enemy=draw_as_enemy) + ' '
        fleet = fleet[:-1]
        fleet += '\n'
        for ship in row2:
            fleet += ship.ship_to_str(draw_as_enemy=draw_as_enemy) + ' '
        fleet = fleet[:-1]
        return fleet

    def get_display_fleet(self, display_as_enemy=False) -> "Fleet":
        """
        Creates a data fleet representing what the specified player would see
        :param display_as_enemy: if set to True, the data will reflect what the
        enemy would see, otherwise it'll look like what the player should see
        :type display_as_enemy: bool
        :return: a Fleet containing data necessary to draw this board on the
        screen
        """
        if display_as_enemy:
            display_ships = []
            for ship in self._ships:
                if ship.sunk():
                    display_ships.append(ship)
                else:
                    origin = ship.origin()
                    size = ship.size()
                    vertical = ship.vertical()
                    new_ship = Ship(origin, size, vertical)
                    display_ships.append(new_ship)
            return Fleet(display_ships)
        else:
            return Fleet(self._ships)

    def ships(self):
        return self._ships

    def selected_ship(self):
        return self._selected_ship
