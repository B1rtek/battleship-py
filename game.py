import os
from time import sleep

from board import Board, GameBoard
from enemy import Enemy
from fleet import Fleet, field_on_board


def cls():
    """
    Clears the console
    """
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")


class Game:
    """
    Handles the game
    """

    def __init__(self, ui=None):
        """
        Initializes all game objects and variables:
        _player_board: player's GameBoard()
        _enemy_board: enemy's GameBoard()
        _player_fleet: player's Fleet()
        _enemy_fleet: enemy's Fleet()
        _enemy: the enemy itself, as an instance of Enemy()
        _ui: reference to the ui if the game runs in the ui mode
        _placement_board: board on which player prepares his fleet, an instance
        of the Board() class
        _player_move: a variable indicating if the player or the enemy should
        move now. Declared here since ui handles move events in a different way
        _suspended_messages: messages about hit or sunk ships from the previous
        move, displayed after refreshing the console
        """
        self._player_board = None
        self._enemy_board = None
        self._player_fleet = None
        self._enemy_fleet = None
        self._enemy = Enemy()
        self._ui = ui
        if self._ui is not None:
            # ui setup
            pass
        self._placement_board = Board()
        self._players_turn = True
        self._suspended_messages = []

    def setup_player_board(self):
        """
        Lets player place their ships however they want, and exits when
        player decides that it's done. In UI mode, it just prepares all
        variables needed for player to see what's going on, as everything is
        handled by buttons in the ui itself.
        """
        self._player_fleet = Fleet()
        self._player_fleet.create_random()
        if self._ui is None:
            while True:
                self._placement_board.place_fleet(self._player_fleet)
                self._refresh_setup()
                self._show_suspended_messages()
                command = input("> ")
                result = self._interpret_and_execute_command(command)
                if result:  # the command was "done"
                    break

    def _refresh_setup(self):
        """
        Refreshes the console content in the setup phase
        """
        cls()
        print(self._placement_board)
        print(self._player_fleet.fleet_to_str())

    def _show_suspended_messages(self):
        """
        Shows suspended messages
        """
        for message in self._suspended_messages:
            print(message)
        self._suspended_messages.clear()

    def _offer_help(self):
        """
        Shows the default "unknown command" message
        """
        offer = "Unknown command. Type \"help\" to get a list of available " \
                "commands"
        self._suspended_messages.append(offer)

    def _bad_syntax(self):
        """
        Shows the default "bad syntax" message
        """
        error = "Wrong command syntax. Type \"help\" to get a list of " \
                "available commands"
        self._suspended_messages.append(error)

    def _setup_show_help(self):
        """
        Shows all setup commands and the correct way to use them
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
                       "current board as the board for the game"
        if self._ui is not None:
            pass
            return
        self._suspended_messages.append(help_content)

    def _setup_select_ship(self, button, x: str = "", y: int = 0):
        """
        An additional method to make using Fleet class commands accessible to
        both ui and console versions of the game
        :param button: ui button, passed as an argument from the button click
        in the ui
        :param x: x coordinate of the field, used by the console version
        :type x: str
        :param y: y coordinate of the field, used by the console version
        :type y: int
        """
        if self._ui is not None:
            pass
            self._placement_board.place_fleet(self._player_fleet)
            return
        result = self._player_fleet.select_ship(x, y)
        self._suspended_messages.append(result)

    def _setup_set_ship_position(self, button, x: str = "", y: int = 0):
        """
        An additional method to make using Fleet class commands accessible to
        both ui and console versions of the game
        :param button: ui button, passed as an argument from the button click
        in the ui
        :param x: x coordinate of the field, used by the console version
        :type x: str
        :param y: y coordinate of the field, used by the console version
        :type y: int
        """
        if self._ui is not None:
            pass
            self._placement_board.place_fleet(self._player_fleet)
            return
        result = self._player_fleet.set_ship_position(x, y)
        self._suspended_messages.append(result)

    def _setup_change_ship_rotation(self):
        """
        An additional method to make using Fleet class commands accessible to
        both ui and console versions of the game
        """
        result = self._player_fleet.change_ship_rotation()
        if self._ui is not None:
            self._placement_board.place_fleet(self._player_fleet)
            return
        self._suspended_messages.append(result)

    def _setup_random_fleet(self):
        """
        Creates a new random fleet. An additional method to make using Fleet
        class commands accessible to both ui and console versions of the game
        """
        self._player_fleet.create_random()
        if self._ui is not None:
            self._placement_board.place_fleet(self._player_fleet)

    def _interpret_and_execute_command(self, whole_command: str):
        """
        Interprets the user's commands.
        :param whole_command: the whole command given by the user.
        :return: True if the command was "done", False otherwise. It's used to
        determine when player has ended the setup process.
        """
        try:
            command = whole_command.split()[0]
        except IndexError:
            self._offer_help()
            return False
        if command == "sel":
            try:
                command, x, s_y = whole_command.split()
                y = int(s_y)
                self._setup_select_ship(None, x, y)
            except ValueError:
                self._bad_syntax()
        elif command == "mv":
            try:
                command, x, s_y = whole_command.split()
                y = int(s_y)
                self._setup_set_ship_position(None, x, y)
            except ValueError:
                self._bad_syntax()
        elif command == "rot":
            self._setup_change_ship_rotation()
        elif command == "done":
            return True
        elif command == "rand":
            self._setup_random_fleet()
        elif command == "help":
            self._setup_show_help()
        else:
            self._offer_help()
        return False

    def start_game(self):
        """
        Sets up enemy board and places player fleet on their board
        """
        self._player_board = GameBoard(self._placement_board)
        self._enemy_fleet = Fleet()
        self._enemy_fleet.create_random()
        enemy_placement_board = Board()
        enemy_placement_board.place_fleet(self._enemy_fleet)
        self._enemy_board = GameBoard(enemy_placement_board)
        self.game_loop()

    def game_loop(self):
        """
        The main game loop which handles player's moves
        """
        self._refresh_board()
        while self._player_fleet.is_alive() and self._enemy_fleet.is_alive():
            if self._players_turn:
                self._player_move()
            else:
                self._advance_game()
                self._enemy_move()
            self._refresh_board()
            self._show_suspended_messages()
        if self._player_fleet.is_alive():
            self._win("You win!")
        else:
            self._win("Computer wins!")

    def _refresh_board(self):
        """
        Method used to print the boards or update the contents of the boards
        in the ui
        """
        if self._ui is not None:
            pass
            return
        cls()
        print(self._enemy_fleet.fleet_to_str(draw_as_enemy=True))
        self._enemy_board.print_board(draw_as_enemy=True)
        print('-' * 20)
        self._player_board.print_board()
        print(self._player_fleet.fleet_to_str())

    def _advance_game(self):
        """
        A method improving feedback for the enemy's actions for the player
        """
        if self._ui is None:
            input("Press a key to advance to the next enemy move...")
        else:
            # a delay to make the action seem more human-like
            sleep(1)

    def _enemy_hit_player_ship(self):
        """
        Method that displays message about enemy hitting player's ship
        """
        message = "Enemy has hit one of your ships!"
        if self._ui is not None:
            pass
            return
        self._suspended_messages.append(message)

    def _enemy_sunk_player_ship(self):
        """
        Method that displays message about enemy sinking player's ship
        """
        message = "Enemy has destroyed one of your ships!"
        if self._ui is not None:
            pass
            return
        self._suspended_messages.append(message)

    def _player_hit_enemy_ship(self):
        """
        Method that displays message about player hitting enemy's ship
        """
        message = "You've hit your opponent's ship!"
        if self._ui is not None:
            pass
            return
        self._suspended_messages.append(message)

    def _player_sunk_enemy_ship(self):
        """
        Method that displays message about enemy sinking player's ship
        """
        message = "You've destroyed your opponent's ship!"
        if self._ui is not None:
            pass
            return
        self._suspended_messages.append(message)

    def _interpret_game_command(self, whole_command) -> tuple[str, str, int]:
        """
        Processes the contents of the given command and returns it as parts
        of a tuple that will be used in _player_move()
        :param whole_command: user's input
        :type whole_command: str
        :return: command and its arguments
        """
        try:
            command = whole_command.split()[0]
        except IndexError:
            return "syntax", "0", 0
        if command == "st" or command == "mk":
            try:
                command, x, s_y = whole_command.split()
                y = int(s_y)
                return command, x, y
            except ValueError:
                return "syntax", "0", 0
        else:
            return command, "0", 0

    def _game_discover_field(self, button, x: str = "", y: int = 0) -> bool:
        """
        An additional method to make game commands accessible to both ui and
        console versions of the game
        :param button: ui button, passed as an argument from the button click
        in the ui
        :param x: x coordinate of the field, used by the console version
        :type x: str
        :param y: y coordinate of the field, used by the console version
        :type y: int
        :return: return value of the discover_field() function
        """
        if self._ui is not None:
            pass
            return
        return self._enemy_board.discover_field(x, y)

    def _game_mark_as_empty(self, button, x: str = "", y: int = 0) -> bool:
        """
        An additional method to make game commands accessible to both ui and
        console versions of the game
        :param button: ui button, passed as an argument from the button click
        in the ui
        :param x: x coordinate of the field, used by the console version
        :type x: str
        :param y: y coordinate of the field, used by the console version
        :type y: int
        :return: return value of the mark_as_empty() function
        """
        if self._ui is not None:
            pass
            return
        return self._enemy_board.mark_as_empty(x, y)

    def _game_show_help(self):
        """
        Shows all game commands and the correct way to use them
        """
        help_content = "Help:\n" \
                       "st <x> <y>: shoots at the specified field\n" \
                       "mk <x> <y>: marks the specified field on the " \
                       "enemy's board as empty"
        if self._ui is not None:
            pass
            return
        self._suspended_messages.append(help_content)

    def _player_move(self):
        """
        Handles the player's move
        """
        self._players_turn = False
        whole_command = input("> ")
        command, x, y = self._interpret_game_command(whole_command)
        if y != 0:
            if not field_on_board((x, y)):
                self._players_turn = True
                message = "Invalid field"
                self._suspended_messages.append(message)
                return
        if command == "st":
            hit = self._game_discover_field(None, x, y)
            if hit:
                self._players_turn = True
                self._player_hit_enemy_ship()
                sunk = self._enemy_fleet.hit(x, y)
                if sunk:
                    self._player_sunk_enemy_ship()
                    ship_to_sink = self._enemy_fleet.find_ship(x, y)
                    self._enemy_board.sink_ship(ship_to_sink)
        elif command == "mk":
            self._players_turn = True
            marked = self._game_mark_as_empty(None, x, y)
            if not marked:
                message = "The field you tried to mark has a discovered ship"
                self._suspended_messages.append(message)
        elif command == "help":
            self._players_turn = True
            self._game_show_help()
        else:
            self._players_turn = True
            self._offer_help()

    def _enemy_move(self):
        """
        Handles the computer enemy's move
        """
        self._players_turn = True
        target = self._enemy.shoot()
        x, y = target
        hit = self._player_board.discover_field(x, y)
        if hit:
            self._players_turn = False
            self._enemy_hit_player_ship()
            sunk = self._player_fleet.hit(x, y)
            self._enemy.react_to_hit()
            if sunk:
                self._enemy_sunk_player_ship()
                ship_to_sink = self._player_fleet.find_ship(x, y)
                self._player_board.sink_ship(ship_to_sink)
                self._enemy.react_to_sink()
        to_mark_as_empty = self._enemy.mark_as_empty()
        if to_mark_as_empty:
            for field in to_mark_as_empty:
                m_x, m_y = field
                self._player_board.mark_as_empty(m_x, m_y)

    def _win(self, winner):
        if self._ui is not None:
            pass
            return
        print(winner)


def main():
    game = Game()
    game.setup_player_board()
    game.start_game()


if __name__ == "__main__":
    main()
