from board import GameBoard, Board
from enemy import Enemy
from fleet import Fleet, field_on_board


class Gamev2:
    """
    Handles the game
    """

    def __init__(self):
        """
        Creates game objects and variables needed to run the game
        """
        self._player_board = None
        self._enemy_board = None
        self._player_fleet = None
        self._enemy_fleet = None
        self._enemy = Enemy()
        self._players_turn = True
        self._won = False
        self._messages = []

    def start_game(self, player_board: Board, player_fleet: Fleet):
        """
        Starts the game by assigning boards and fleets
        :param player_board: player's board, created in the setup phase
        :type player_board: GameBoard
        :param player_fleet: player's fleet, also from the setup phase
        :type player_fleet: Fleet
        """
        self._player_board = GameBoard(player_board)
        self._player_fleet = player_fleet
        self._create_enemy_fleet()
        self._players_turn = True
        self._won = False

    def _create_enemy_fleet(self):
        """
        Creates enemy's fleet and board
        """
        self._enemy_fleet = Fleet()
        self._enemy_fleet.create_random()
        enemy_board = Board()
        enemy_board.place_fleet(self._enemy_fleet)
        self._enemy_board = GameBoard(enemy_board)

    def get_player_board_display(self) -> Board:
        """
        Returns player's board to display
        """
        return self._player_board.get_display_board()

    def get_enemy_board_display(self) -> Board:
        """
        Returns enemy's board to display
        """
        return self._enemy_board.get_display_board(display_as_enemy=True)

    def get_player_fleet_display(self) -> Fleet:
        """
        Returns player's fleet
        """
        return self._player_fleet.get_display_fleet()

    def get_enemy_fleet_display(self) -> Fleet:
        """
        Returns enemy's fleet
        """
        return self._enemy_fleet.get_display_fleet(display_as_enemy=False)

    def get_display_messages(self):
        """
        Returns the messages that the player received in this turn
        """
        return self._format_messages()

    def _format_messages(self):
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

    def _message_not_players_turn(self):
        """
        Adds the message about player turning while the enemy should to the
        messages list
        """
        self._messages.append("It's not your turn!")

    def _message_invalid_coordinates(self):
        """
        Adds the message about invalid field coordinates to the messages list
        """
        self._messages.append("Invalid field coordinates")

    def _message_enemy_ship_hit(self):
        """
        Adds the message about hitting enemy's ship to the messages list
        """
        self._messages.append("You've hit an enemy ship!")

    def _message_enemy_ship_sunk(self):
        """
        Adds the message about sinking enemy's ship to the messages list
        """
        self._messages.append("You've destroyed an enemy ship!")

    def _message_enemy_miss(self):
        """
        Adds the message about enemy missing the shot to the messages list
        """
        self._messages.append("Enemy has missed.")

    def _message_enemy_win(self):
        """
        Adds the message about enemy winning the game to the messages list
        """
        self._messages.append("Enemy wins.")

    def _message_field_mark_fail(self):
        """
        Adds the message about trying to mark a field that cannot be marked to
        the messages list
        """
        self._messages.append("The field you tried to mark has a discovered "
                              "ship")

    def _message_field_unmark_fail(self):
        """
        Adds the message about trying to unmark a field that is not marked to
        the messages list
        """
        self._messages.append("The field you tried to unmark isn't marked")

    def _message_game_help(self):
        """
        Adds the game help content to the messages list
        """
        help_content = "Help:\n" \
                       "st <x> <y>: shoots at the specified field\n" \
                       "mk <x> <y>: marks the specified field on the " \
                       "enemy's board as empty\n" \
                       "unmk <x> <y>: unmarks the specified field\n" \
                       "quit: quits the game"
        self._messages.append(help_content)

    def _message_player_ship_hit(self):
        """
        Adds the message about enemy hitting player's ship to the messages list
        """
        self._messages.append("Enemy has hit one of your ships!")

    def _message_player_ship_sunk(self):
        """
        Adds the message about enemy sinking player's ship to the messages list
        """
        self._messages.append("Enemy has destroyed one of your ships!")

    def _message_player_miss(self):
        """
        Adds the message about player missing the shot to the messages list
        """
        self._messages.append("You missed.")

    def _message_player_win(self):
        """
        Adds the message about player winning the game to the messages list
        """
        self._messages.append("You win!")

    def discover_field(self, x: str, y: int) -> bool:
        """
        Handles the field discovery process for the player
        :param x: x coordinate of a field
        :type x: str
        :param y: y coordinate of a field
        :type y: int
        :return: True if the player hit enemy's ship, otherwise false.
        """
        if not self._players_turn:
            self._message_not_players_turn()
            return False
        if not field_on_board((x, y)):
            self._message_invalid_coordinates()
            return True
        self._players_turn = False
        hit = self._enemy_board.discover_field(x, y)
        if hit:
            self._players_turn = True
            self._message_enemy_ship_hit()
            sunk = self._enemy_fleet.hit(x, y)
            if sunk:
                self._message_enemy_ship_sunk()
                ship_to_sink = self._enemy_fleet.find_ship(x, y)
                self._enemy_board.sink_ship(ship_to_sink)
                self._check_win()
        else:
            self._message_player_miss()
        return hit

    def mark_field(self, x: str, y: int):
        """
        Handles the field marking process for the player
        :param x: x coordinate of a field
        :type x: str
        :param y: y coordinate of a field
        :type y: int
        """
        if not field_on_board((x, y)):
            self._message_invalid_coordinates()
            return
        marked = self._enemy_board.mark_as_empty(x, y)
        if not marked:
            self._message_field_mark_fail()

    def unmark_field(self, x: str, y: int):
        """
        Handles the field unmarking process for the player
        :param x: x coordinate of a field
        :type x: str
        :param y: y coordinate of a field
        :type y: int
        """
        if not field_on_board((x, y)):
            self._message_invalid_coordinates()
            return
        unmarked = self._enemy_board.unmark_as_empty(x, y)
        if not unmarked:
            self._message_field_unmark_fail()

    def game_help(self):
        """
        Handles the help command output
        """
        self._message_game_help()

    def enemy_move(self) -> bool:
        """
        Handles the computer enemy's move
        :return: True if the enemy hit player's ship, otherwise false.
        """
        self._players_turn = True
        target = self._enemy.shoot()
        x, y = target
        hit = self._player_board.discover_field(x, y)
        if hit:
            self._players_turn = False
            self._message_player_ship_hit()
            sunk = self._player_fleet.hit(x, y)
            self._enemy.react_to_hit()
            if sunk:
                self._message_player_ship_sunk()
                ship_to_sink = self._player_fleet.find_ship(x, y)
                self._player_board.sink_ship(ship_to_sink)
                self._enemy.react_to_sink()
                self._check_win()
        else:
            self._message_enemy_miss()
        to_mark_as_empty = self._enemy.mark_as_empty()
        if to_mark_as_empty:
            for field in to_mark_as_empty:
                m_x, m_y = field
                self._player_board.mark_as_empty(m_x, m_y)

        return hit

    def _check_win(self):
        """
        Checks if one of the players won the game
        """
        if not self._player_fleet.is_alive():
            self._message_enemy_win()
            self._won = True
        if not self._enemy_fleet.is_alive():
            self._message_player_win()
            self._won = True

    def players_turn(self) -> bool:
        return self._players_turn

    def won(self) -> bool:
        return self._won

