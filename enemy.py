from copy import deepcopy
from random import choice


def create_list_of_adherent(source: tuple[str, int]) -> list:
    x, y = source
    return [(chr(ord(x) - 1), y), (x, y - 1), (chr(ord(x) + 1), y),
            (x, y + 1)]


def create_list_of_tangents(source: tuple[str, int]) -> list:
    x, y = source
    return [(chr(ord(x) - 1), y - 1), (chr(ord(x) + 1), y - 1),
            (chr(ord(x) - 1), y + 1), (chr(ord(x) + 1), y + 1)]


class Enemy:
    """
    Class representing the computer opponent
    """

    def __init__(self):
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
        for x in "abcdefghij":
            for y in range(1, 11):
                self._undiscovered.append((x, y))
        self._last_target = None

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
        chosen = choice(self._undiscovered)
        self._undiscovered.remove(chosen)
        self._last_target = chosen
        return chosen

    def react_to_hit(self):
        """
        Marks fields that can't have any ships as empty and puts new targets
        on the to_shoot list
        """
        to_mark_as_empty_list = create_list_of_tangents(self._last_target)
        for target in to_mark_as_empty_list:
            if target in self._undiscovered:
                self._undiscovered.remove(target)
                self._to_mark_as_empty.append(target)
        to_shoot_list = create_list_of_adherent(self._last_target)
        for target in to_shoot_list:
            if target in self._undiscovered:
                self._to_shoot.append(target)

    def react_to_sink(self):
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
