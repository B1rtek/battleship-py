from board import Board
from fleet import Fleet


class FleetCreator:
    """
    Class handling player board's setup in the setup phase of the game
    """

    def __init__(self):
        """
        Creates game objects and variables needed to operate the fleet creator
        """
        self._board = Board()
        self._fleet = Fleet()
        self._messages = []

    def start(self):
        """
        Starts the Fleet Creator by creating a new random fleet and placing it
        on the board
        """
        self._fleet.create_random()
        self._board.place_fleet(self._fleet)

    def get_board_display(self) -> Board:
        """
        :return: Board with the representation of the current Fleet setup
        """
        return self._board

    def get_setup(self) -> tuple[Board, Fleet]:
        """
        :return: a tuple of the Board and Fleet created in the Fleet Creator,
        called when the played uses the "done" command or clicks the "Done"
        button
        """
        return self._board, self._fleet

    def get_display_messages(self) -> str:
        """
        A getter for the messages list used by the Battleship classes to get
        the messages to display
        :return: a string with all messages generated during the last operation
        """
        return self._format_messages()

    def _format_messages(self) -> str:
        """
        Creates a string out of the messages on the list, and clears the
        list afterwards
        :return: messages formatted in a string
        """
        formatted_messages = ""
        for message in self._messages:
            formatted_messages += message
            formatted_messages += '\n'
        self._messages.clear()
        return formatted_messages

    def _message_ship_selected(self):
        """
        Adds the message about ship being selected to the messages list
        """
        self._messages.append("A ship has been selected")

    def _message_ship_move_fail(self):
        """
        Adds the message about failing to move a ship to the messages list
        """
        self._messages.append("The selected location is invalid")

    def _message_ship_rotation_fail(self):
        """
        Adds the message about failing to rotate a ship to the messages list
        """
        self._messages.append("You can't rotate this ship")

    def _message_setup_help(self):
        """
        Adds the setup help content to the messages list
        """
        help_content = "Help:\n" \
                       "sel <x> <y>: Selects a ship in the given location\n" \
                       "mv <x> <y>: Moves the selected ship to the given " \
                       "location. The location points to the ship's " \
                       "uppermost or left segment\n" \
                       "rot: Rotates the selected ship from vertical to " \
                       "horizontal rotation, or the other way, around it's " \
                       "uppermost or left part\n" \
                       "rand: Places all ships randomly\n" \
                       "done: Ends the setup process and accepts the " \
                       "current board as the board for the game\n" \
                       "quit: exits to main menu"
        self._messages.append(help_content)

    def select_ship(self, x: str, y: int):
        """
        Handles the ship selection in the board setup process
        :param x: x coordinate of the field
        :type x: str
        :param y: y coordinate of the field
        :type y: int
        """
        result = self._fleet.select_ship(x, y)
        if result:
            self._message_ship_selected()

    def set_ship_position(self, x: str, y: int):
        """
        Handles the ship position setting in the board setup process
        :param x: x coordinate of the field
        :type x: str
        :param y: y coordinate of the field
        :type y: int
        """
        result = self._fleet.set_ship_position(x, y)
        if not result:
            self._message_ship_move_fail()
        else:
            self._board.place_fleet(self._fleet)

    def change_ship_rotation(self):
        """
        Handles the selected ship rotation change
        """
        result = self._fleet.change_ship_rotation()
        if not result:
            self._message_ship_rotation_fail()
        else:
            self._board.place_fleet(self._fleet)

    def random_fleet(self):
        """
        Handles the creation of a new random fleet
        """
        self._fleet.create_random()
        self._board.place_fleet(self._fleet)

    def setup_help(self):
        """
        Handles the help command output
        """
        self._message_setup_help()

    def get_selected_ship(self):
        """
        Returns the selected ship from the fleet
        :return: The selected ship in the setup fleet (can be None)
        """
        return self._fleet.selected_ship()

    def contains_not_selected_ship(self, x: str, y: int) -> bool:
        """
        Checks if the specified field contains a ship that is not selected.
        Used in the UI version of the game to determine if the player selected
        or wanted to move a ship
        :param x: x coordinate of the field
        :type x: str
        :param y: y coordinate of the field
        :type y: int
        :return: True if this ship does not contain a ship or contains a
        selected one, False otherwise
        """
        if self._fleet.selected_ship() is None:
            return True
        if self._fleet.selected_ship().check_if_belongs(x, y):
            return False
        if self._fleet.find_ship(x, y) is not None:
            return True
        return False
