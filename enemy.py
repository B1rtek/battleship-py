from copy import deepcopy
from random import choice, shuffle

import board


def create_list_of_adherent(source: tuple[str, int]) -> list:
    """
    Creates a list of tuples representing coordinates of fields that would be
    adherent to a field with coordinates provided in the source tuple
    :param source: tuple containing coordinates of a field
    :type source: tuple
    :return: list of tuples containing coordinates of fields that would be
    adherent to the given one
    """
    return [left_field(source), right_field(source), upper_field(source),
            lower_field(source)]


def create_list_of_tangents(source: tuple[str, int]) -> list:
    """
    Creates a list of tuples representing coordinates of fields that would
    touch the field with provided coordinates with only their corner
    :param source: tuple containing coordinates of a field
    :type source: tuple
    :return: list of tuples containing coordinates of fields that touch the
    source field's corners
    """
    return [left_field(upper_field(source)), right_field(upper_field(source)),
            left_field(lower_field(source)), right_field(lower_field(source))]


def upper_field(coords: tuple[str, int]) -> tuple[str, int]:
    x, y = coords
    return x, y - 1


def lower_field(coords: tuple[str, int]) -> tuple[str, int]:
    x, y = coords
    return x, y + 1


def left_field(coords: tuple[str, int]) -> tuple[str, int]:
    x, y = coords
    return chr(ord(x) - 1), y


def right_field(coords: tuple[str, int]) -> tuple[str, int]:
    x, y = coords
    return chr(ord(x) + 1), y


class Enemy:
    """
    Class representing the computer opponent
    """

    def __init__(self, hard_mode: bool = False):
        """
        Creates an Enemy class, initializing 3 lists - a list of undiscovered
        fields which Enemy will shoot randomly at, a list of to_shoot fields,
        which have higher priority than random targets and are set once a ship
        is hit, and to_mark_as_empty list, which gets populated by fields to
        mark as empty once a ship is hit
        """
        self._undiscovered = []
        self._to_shoot = []
        self._to_mark_as_empty = []
        for x, y in board.return_all_field_coordinates():
            self._undiscovered.append((x, y))
        self._last_target = None
        self._hard_mode = hard_mode

    def shoot(self) -> tuple[str, int]:
        """
        Chooses a field that will be shot at
        :return: a tuple with field coordinates
        """
        while self._to_shoot:
            chosen = self._to_shoot[0]
            self._to_shoot.remove(chosen)
            if chosen in self._undiscovered:
                self._undiscovered.remove(chosen)
                self._last_target = chosen
                return chosen
        if self._hard_mode:
            chosen = self._rank_fields_and_choose()
        else:
            chosen = choice(self._undiscovered)
        self._undiscovered.remove(chosen)
        self._last_target = chosen
        return chosen

    def _rank_fields_and_choose(self) -> tuple[str, int]:
        """
        Creates a list of fields sorted by the maximum length of a ship that
        can be located there, and then returns coordinates of one with the
        highest score
        """
        rank_list = []
        for field in self._undiscovered:
            score_vert = 1
            score_horiz = 1
            current = deepcopy(field)
            current = upper_field(current)
            while current in self._undiscovered:
                score_vert = score_vert + 1
                current = upper_field(current)
            current = deepcopy(field)
            current = lower_field(current)
            while current in self._undiscovered:
                score_vert = score_vert + 1
                current = lower_field(current)
            current = deepcopy(field)
            current = right_field(current)
            while current in self._undiscovered:
                score_horiz = score_horiz + 1
                current = right_field(current)
            current = deepcopy(field)
            current = left_field(current)
            while current in self._undiscovered:
                score_horiz = score_horiz + 1
                current = left_field(current)
            rank_list.append((max(score_vert, score_horiz), field))
        # awkward sorting because sorted() doesn't want to work
        best_fields = []
        max_score = max(x[0] for x in rank_list)
        for score, field in rank_list:
            if score == max_score:
                best_fields.append(field)
        return choice(best_fields)

    def react_to_hit(self):
        """
        Appends coordinates of fields that can't have any ships to the
        _to_mark_as_empty list and puts new targets on the _to_shoot list
        """
        to_mark_as_empty_list = create_list_of_tangents(self._last_target)
        for target in to_mark_as_empty_list:
            if target in self._undiscovered:
                self._undiscovered.remove(target)
                self._to_mark_as_empty.append(target)
        to_shoot_list = create_list_of_adherent(self._last_target)
        shuffle(to_shoot_list)
        for target in to_shoot_list:
            if target in self._undiscovered:
                self._to_shoot.append(target)

    def react_to_sink(self):
        """
        Appends all the remaining unmarked fields around a sunken ship to the
        _to_mark_as_empty list
        """
        to_mark_as_empty_list = create_list_of_adherent(self._last_target)
        for target in to_mark_as_empty_list:
            if target in self._undiscovered:
                self._undiscovered.remove(target)
                self._to_mark_as_empty.append(target)
        for target in self._to_shoot:
            self._to_mark_as_empty.append(target)
        self._to_shoot.clear()

    def mark_as_empty(self) -> list:
        """
        Returns a list of fields to mark as empty after a move
        :return: a list of fields to mark as empty
        """
        to_mark_as_empty_list = deepcopy(self._to_mark_as_empty)
        self._to_mark_as_empty.clear()
        return to_mark_as_empty_list
