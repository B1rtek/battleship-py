from enum import Enum


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

    def __str__(self):
        """
        Used to print out the fields in the console
        """
        if self._status == FieldStatus.NOTHING:
            return ' '
        elif self._status == FieldStatus.MISS:
            return '.'
        elif self._status == FieldStatus.SHIP:
            return '█'
        else:  # FieldStatus.SUNK
            return 'X'

    def status(self):
        return self._status

    def set_status(self, new_status: FieldStatus):
        self._status = new_status
