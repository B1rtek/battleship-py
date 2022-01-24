from copy import deepcopy
from enum import Enum

from board import GameBoard, Board, field_on_board
from enemy import Enemy
from fleet import Fleet
from settings import Setting, Settings


class GameMessage(Enum):
    NOT_PLAYERS_TURN = 0,
    INVALID_COORDS = 1,
    ENEMY_SHIP_HIT = 2,
    ENEMY_SHIP_SUNK = 3,
    ENEMY_MISS = 4,
    ENEMY_WIN = 5,
    FIELD_MARK_FAIL = 6,
    FIELD_UNMARK_FAIL = 7,
    GAME_HELP = 8,
    PLAYER_SHIP_HIT = 9,
    PLAYER_SHIP_SUNK = 10,
    PLAYER_MISS = 11,
    PLAYER_WIN = 12,
    FIELD_ALREADY_DISCOVERED = 13,
    PLAYERS_TURN = 14


class Game:
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
        self._enemy = None
        self._players_turn = True
        self._won = False
        self._messages = []
        self._settings = None
        self.apply_settings(None)

    def apply_settings(self, settings: dict = None):
        if settings is None:
            default_settings = Settings()
            self._settings = default_settings.get_settings()
        else:
            self._settings = settings

    def _create_enemy_fleet(self):
        """
        Creates enemy's fleet and board
        """
        self._enemy_fleet = Fleet()
        self._enemy_fleet.create_random()
        enemy_board = Board()
        enemy_board.place_fleet(self._enemy_fleet)
        self._enemy_board = GameBoard(enemy_board)

    def start_game(self, player_board: Board, player_fleet: Fleet):
        """
        Starts the game by assigning boards and fleets
        :param player_board: player's board, created in the setup phase
        :type player_board: GameBoard
        :param player_fleet: player's fleet, also from the setup phase
        :type player_fleet: Fleet
        """
        self._player_board = GameBoard(player_board)
        self._enemy = Enemy(self._settings[Setting.HARD_ENEMY])
        self._player_fleet = player_fleet
        self._create_enemy_fleet()
        self._players_turn = True
        self._won = False
        self._message_players_turn()

    def discover_field(self, x: str, y: int) -> bool:
        """
        Handles the field discovery process for the player
        :param x: x coordinate of a field
        :type x: str
        :param y: y coordinate of a field
        :type y: int
        :return: True if the player hit enemy's ship, otherwise false. True is
        also returned when the move failed because of discovering fields on
        coordinates outside the board or fields already discovered, to
        prevent the player from losing their turn
        """
        if not self._players_turn:
            self._message_not_players_turn()
            return False
        if not field_on_board((x, y)):
            self._message_invalid_coordinates()
            return True
        if not self._enemy_board.field_undiscovered(x, y):
            self._message_field_already_discovered()
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
                if self._settings[Setting.MARK_MISSES_AROUND]:
                    self._enemy_board.mark_misses_around(ship_to_sink)
                self.check_win()
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
        if self._players_turn:
            return False
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
                self.check_win()
        else:
            self._players_turn = True
            self._message_enemy_miss()
        to_mark_as_empty = self._enemy.mark_as_empty()
        if to_mark_as_empty:
            for field in to_mark_as_empty:
                m_x, m_y = field
                self._player_board.mark_as_empty(m_x, m_y)
        return hit

    def check_win(self) -> bool:
        """
        Checks if one of the players won the game
        :return: True if the player won, False if the computer enemy won
        """
        if not self._player_fleet.is_alive():
            self._message_enemy_win()
            self._won = True
            return False
        if not self._enemy_fleet.is_alive():
            self._message_player_win()
            self._won = True
            return True

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
        return self._enemy_fleet.get_display_fleet(display_as_enemy=True)

    def _message_not_players_turn(self):
        """
        Adds the message about player turning while the enemy should to the
        messages list
        """
        self._messages.append(GameMessage.NOT_PLAYERS_TURN)

    def _message_invalid_coordinates(self):
        """
        Adds the message about invalid field coordinates to the messages list
        """
        self._messages.append(GameMessage.INVALID_COORDS)

    def _message_enemy_ship_hit(self):
        """
        Adds the message about hitting enemy's ship to the messages list
        """
        self._messages.append(GameMessage.ENEMY_SHIP_HIT)

    def _message_enemy_ship_sunk(self):
        """
        Adds the message about sinking enemy's ship to the messages list
        """
        self._messages.append(GameMessage.ENEMY_SHIP_SUNK)

    def _message_enemy_miss(self):
        """
        Adds the message about enemy missing the shot to the messages list
        """
        self._messages.append(GameMessage.ENEMY_MISS)

    def _message_enemy_win(self):
        """
        Adds the message about enemy winning the game to the messages list
        """
        self._messages.append(GameMessage.ENEMY_WIN)

    def _message_field_mark_fail(self):
        """
        Adds the message about trying to mark a field that cannot be marked to
        the messages list
        """
        self._messages.append(GameMessage.FIELD_MARK_FAIL)

    def _message_field_unmark_fail(self):
        """
        Adds the message about trying to unmark a field that is not marked to
        the messages list
        """
        self._messages.append(GameMessage.FIELD_UNMARK_FAIL)

    def _message_game_help(self):
        """
        Adds the game help content to the messages list
        """
        self._messages.append(GameMessage.GAME_HELP)

    def _message_player_ship_hit(self):
        """
        Adds the message about enemy hitting player's ship to the messages list
        """
        self._messages.append(GameMessage.PLAYER_SHIP_HIT)

    def _message_player_ship_sunk(self):
        """
        Adds the message about enemy sinking player's ship to the messages list
        """
        self._messages.append(GameMessage.PLAYER_SHIP_SUNK)

    def _message_player_miss(self):
        """
        Adds the message about player missing the shot to the messages list
        """
        self._messages.append(GameMessage.PLAYER_MISS)

    def _message_player_win(self):
        """
        Adds the message about player winning the game to the messages list
        """
        self._messages.append(GameMessage.PLAYER_WIN)

    def _message_field_already_discovered(self):
        """
        Adds the message about player trying to discover an already discovered
        field to the messages list
        """
        self._messages.append(GameMessage.FIELD_ALREADY_DISCOVERED)

    def _message_players_turn(self):
        """
        Adds the message about player's turn to the messages list
        """
        self._messages.append(GameMessage.PLAYERS_TURN)

    def get_display_messages(self) -> list:
        """
        A getter for the messages list used by the Battleship classes to get
        the messages to display
        :return: a list with all messages generated during the last move
        """
        messages = deepcopy(self._messages)
        self._messages.clear()
        return messages

    def players_turn(self) -> bool:
        return self._players_turn

    def won(self) -> bool:
        return self._won
