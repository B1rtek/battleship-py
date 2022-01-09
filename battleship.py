import argparse
import os
import sys
import time
from enum import Enum
from functools import partial

from PySide2.QtCore import Qt
from PySide2.QtWidgets import QApplication, QMainWindow

from board import GameBoard, Board, FieldStatus
from gui import UIBoard, load_icons, UIFleet
from fleet_creator import FleetCreator
from game import Game
from ui_battleship import Ui_Battleship


class AppState(Enum):
    MAIN_MENU = 0,
    SETUP = 1,
    GAME = 2,
    HOW_TO_PLAY = 3


class Command(Enum):
    NOP = 0,
    MAIN_START_SETUP = 1,
    MAIN_START_HTP = 2,
    MAIN_EXIT = 3,
    EXIT_TO_MAIN = 4,
    CREATOR_SHIP_SELECT = 5,
    CREATOR_SHIP_MOVE = 6,
    CREATOR_SHIP_ROTATE = 7,
    CREATOR_FLEET_RAND = 8,
    CREATOR_DONE = 9,
    CREATOR_HELP = 10,
    GAME_SHOOT = 11,
    GAME_MARK_FIELD = 12,
    GAME_UNMARK_FIELD = 13,
    GAME_HELP = 14


def cls():
    """
    Clears the console
    """
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")


class BattleshipCMD:
    """
    Class operating the game in the command line
    """

    def __init__(self):
        """
        Initializes classes handling the actual game
        """
        self._fleet_creator = FleetCreator()
        self._game = Game()
        self._state = AppState.MAIN_MENU
        self._quit = False
        self._prompt = "> "

    def _display(self):
        """
        Displays content in the console
        """
        cls()
        if self._state == AppState.MAIN_MENU:
            self._display_main_menu()
        elif self._state == AppState.SETUP:
            self._display_fleet_creator()
        elif self._state == AppState.GAME:
            self._display_game()
        else:  # AppState.HOW_TO_PLAY
            self._display_help()

    def _display_main_menu(self):
        menu_content = "Welcome to Battleship!\n" \
                       "1. Play the game\n" \
                       "2. How to play\n" \
                       "3. Exit\n" \
                       "\n"
        print(menu_content)

    def _display_fleet_creator(self):
        display_board = self._fleet_creator.get_board_display()
        print("Set up your fleet:")
        print(display_board)
        print(self._fleet_creator.get_display_messages())

    def _display_game(self):
        enemy_fleet = self._game.get_enemy_fleet_display()
        enemy_fleet_str = enemy_fleet.fleet_to_str(draw_as_enemy=True)
        enemy_board = self._game.get_enemy_board_display()
        enemy_board_str = str(enemy_board)
        splitter = '-' * 15
        player_board = self._game.get_player_board_display()
        player_board_str = str(player_board)
        player_fleet = self._game.get_player_fleet_display()
        player_fleet_str = player_fleet.fleet_to_str()
        messages = self._game.get_display_messages()
        print(enemy_fleet_str)
        print(enemy_board_str)
        print(splitter)
        print(player_board_str)
        print(player_fleet_str)
        print(messages)

    def _display_help(self):
        help_content = "How to play:\n" \
                       "The objective of this game is to destroy your " \
                       "opponent's fleet. You and your opponent shoot at " \
                       "chosen fields on the board, and get information " \
                       "whether you've hit or sunk you enemy's ship. If " \
                       "there was a hit, the player gets another move, if " \
                       "there isn't, the enemy gets to move.\n"
        print(help_content)

    def _player_input(self) -> tuple[Command, str, int]:
        """
        Handles user input and interprets it, creating a command
        :return: tuple containing a command and arguments
        """
        whole_command = input(self._prompt)
        whole_command = whole_command.lower()
        command_parts = whole_command.split()
        if self._state == AppState.MAIN_MENU:
            return self._player_input_main_menu(command_parts)
        elif self._state == AppState.SETUP:
            return self._player_input_fleet_creator(command_parts)
        elif self._state == AppState.GAME:
            return self._player_input_game(command_parts)
        else:
            return Command.EXIT_TO_MAIN, "", 0

    def _player_input_main_menu(self, command_parts: list[str]) -> \
            tuple[Command, str, int]:
        """
        Interprets the main menu commands
        :param command_parts: sliced user input
        :return: formatted command
        """
        if len(command_parts) == 0:
            return Command.NOP, "", 0
        else:
            if command_parts[0].startswith('1'):
                return Command.MAIN_START_SETUP, "", 0
            elif command_parts[0].startswith('2'):
                return Command.MAIN_START_HTP, "", 0
            elif command_parts[0].startswith('3'):
                return Command.MAIN_EXIT, "", 0
            else:
                return Command.NOP, "", 0

    def _player_input_fleet_creator(self, command_parts: list[str]) -> \
            tuple[Command, str, int]:
        """
        Interprets the fleet creator commands
        :param command_parts: sliced user input
        :return: formatted command
        """
        if len(command_parts) == 0:
            return Command.NOP, "", 0
        if command_parts[0] == "rot":
            return Command.CREATOR_SHIP_ROTATE, "", 0
        elif command_parts[0] == "rand":
            return Command.CREATOR_FLEET_RAND, "", 0
        elif command_parts[0] == "done":
            return Command.CREATOR_DONE, "", 0
        elif command_parts[0] == "quit":
            return Command.EXIT_TO_MAIN, "", 0
        elif command_parts[0] == "help":
            return Command.CREATOR_HELP, "", 0
        elif len(command_parts) >= 3:
            x = command_parts[1]
            try:
                y = int(command_parts[2])
            except ValueError:
                return Command.NOP, "", 0
            if command_parts[0] == "sel":
                return Command.CREATOR_SHIP_SELECT, x, y
            elif command_parts[0] == "mv":
                return Command.CREATOR_SHIP_MOVE, x, y
            else:
                return Command.NOP, "", 0
        else:
            return Command.NOP, "", 0

    def _player_input_game(self, command_parts: list[str]) -> \
            tuple[Command, str, int]:
        """
        Interprets the game commands
        :param command_parts: sliced user input
        :return: formatted command
        """
        if len(command_parts) == 0:
            return Command.NOP, "", 0
        if command_parts[0] == "help":
            return Command.GAME_HELP, "", 0
        elif command_parts[0] == "quit":
            return Command.EXIT_TO_MAIN, "", 0
        elif len(command_parts) >= 3:
            x = command_parts[1]
            try:
                y = int(command_parts[2])
            except ValueError:
                return Command.NOP, "", 0
            if command_parts[0] == "st":
                return Command.GAME_SHOOT, x, y
            elif command_parts[0] == "mk":
                return Command.GAME_MARK_FIELD, x, y
            elif command_parts[0] == "unmk":
                return Command.GAME_UNMARK_FIELD, x, y
            else:
                return Command.NOP, "", 0
        else:
            return Command.NOP, "", 0

    def _execute(self, command, x, y):
        """
        Executes user's command
        :param command: command as a Command class enum
        :type command: Command
        :param x: x coordinate of a field (used in some commands)
        :type x: str
        :param y: y coordinate of a field (used in some commands)
        :type y: int
        """
        if self._state == AppState.MAIN_MENU:
            self._execute_main_menu(command)
        elif self._state == AppState.SETUP:
            self._execute_fleet_creator(command, x, y)
        elif self._state == AppState.GAME:
            self._execute_game(command, x, y)
        elif self._state == AppState.HOW_TO_PLAY:
            self._state = AppState.MAIN_MENU

    def _execute_main_menu(self, command):
        """
        Executes main menu commands
        :param command: command as a Command class enum
        :type command: Command
        """
        if command == Command.MAIN_START_SETUP:
            self._fleet_creator.start()
            self._state = AppState.SETUP
        elif command == Command.MAIN_START_HTP:
            self._state = AppState.HOW_TO_PLAY
        elif command == Command.MAIN_EXIT:
            self._quit = True

    def _execute_fleet_creator(self, command, x, y):
        """
        Executes fleet creator commands
        :param command: command as a Command class enum
        :type command: Command
        :param x: x coordinate of a field (used in some commands)
        :type x: str
        :param y: y coordinate of a field (used in some commands)
        :type y: int
        """
        if command == Command.CREATOR_SHIP_SELECT:
            self._fleet_creator.select_ship(x, y)
        elif command == Command.CREATOR_SHIP_MOVE:
            self._fleet_creator.set_ship_position(x, y)
        elif command == Command.CREATOR_SHIP_ROTATE:
            self._fleet_creator.change_ship_rotation()
        elif command == Command.CREATOR_FLEET_RAND:
            self._fleet_creator.random_fleet()
        elif command == Command.CREATOR_DONE:
            board, fleet = self._fleet_creator.get_setup()
            self._game.start_game(board, fleet)
            self._state = AppState.GAME
        elif command == Command.CREATOR_HELP:
            self._fleet_creator.setup_help()
        elif command == Command.EXIT_TO_MAIN:
            self._state = AppState.MAIN_MENU

    def _execute_game(self, command, x, y):
        """
        Executes game commands
        :param command: command as a Command class enum
        :type command: Command
        :param x: x coordinate of a field (used in some commands)
        :type x: str
        :param y: y coordinate of a field (used in some commands)
        :type y: int
        """
        if self._game.won():
            self._state = AppState.MAIN_MENU
        else:
            if not self._game.players_turn():
                self._game.enemy_move()
            else:
                if command == Command.GAME_SHOOT:
                    self._game.discover_field(x, y)
                elif command == Command.GAME_MARK_FIELD:
                    self._game.mark_field(x, y)
                elif command == Command.GAME_UNMARK_FIELD:
                    self._game.unmark_field(x, y)
                elif command == Command.GAME_HELP:
                    self._game.game_help()
                elif command == Command.EXIT_TO_MAIN:
                    self._state = AppState.MAIN_MENU

    def start(self):
        while not self._quit:
            self._display()
            command, x, y = self._player_input()
            self._execute(command, x, y)


class BattleshipWindow(QMainWindow):
    """
    Class operating the game in the GUI version
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Battleship()
        self.ui.setupUi(self)
        self._fleet_creator = FleetCreator()
        self._game = Game()
        self._fleet_creator_board = UIBoard()
        self._game_player_board = UIBoard()
        self._game_enemy_board = UIBoard()
        self._game_player_fleet = UIFleet()
        self._game_enemy_fleet = UIFleet()
        self._setup_boards()
        self._setup_fleet_displays()
        self._link_buttons()
        self._resize_window()
        self._fix_pyside2_uic_bug()
        self.ui.stackedWidget.setCurrentIndex(0)

    def mousePressEvent(self, QMouseEvent):
        if not self._game.players_turn():
            self._game.enemy_move()
            self._game_refresh()
        if self._game.won():
            self.ui.stackedWidget.setCurrentIndex(0)

    def _setup_boards(self):
        icons = load_icons()
        self._fleet_creator_board.set_icons(icons)
        self._game_player_board.set_icons(icons)
        self._game_enemy_board.set_icons(icons)
        self._fleet_creator_board.define_left_click_action(
            self._fleet_creator_left_click)
        self._fleet_creator_board.define_right_click_action(self._nop)
        self._game_player_board.define_left_click_action(self._nop)
        self._game_player_board.define_right_click_action(self._nop)
        self._game_enemy_board.define_left_click_action(
            self._game_left_click)
        self._game_enemy_board.define_right_click_action(
            self._game_right_click)
        self._fleet_creator_board.place_button_array(self.ui.grid_setup_board)
        self._game_player_board.place_button_array(
            self.ui.grid_game_player_board)
        self._game_enemy_board.place_button_array(
            self.ui.grid_game_enemy_board)

    def _setup_fleet_displays(self):
        icons = load_icons()
        self._game_player_fleet.set_icons(icons)
        self._game_enemy_fleet.set_icons(icons)
        self._game_player_fleet.define_left_click_action(self._game_left_click)
        self._game_player_fleet.define_right_click_action(
            self._game_left_click)
        self._game_enemy_fleet.define_left_click_action(self._game_left_click)
        self._game_enemy_fleet.define_right_click_action(self._game_left_click)
        self._game_player_fleet.place_button_array(
            self.ui.grid_game_player_fleet)
        self._game_enemy_fleet.place_button_array(
            self.ui.grid_game_enemy_fleet)

    def _link_buttons(self):
        """
        Assigns functions to different buttons
        """
        self.ui.button_main_play.clicked.connect(self._fleet_creator_start)
        self.ui.button_main_htp.clicked.connect(self._htp_show)
        self.ui.button_main_quit.clicked.connect(partial(sys.exit, 0))
        self.ui.button_setup_exit.clicked.connect(self._return_to_main)
        self.ui.button_setup_rand.clicked.connect(self._fleet_creator_rand)
        self.ui.button_setup_rot.clicked.connect(self._fleet_creator_rot)
        self.ui.button_setup_done.clicked.connect(self._fleet_creator_done)
        self.ui.button_game_main.clicked.connect(self._return_to_main)
        self.ui.button_htp_back.clicked.connect(self._return_to_main)

    def _fix_pyside2_uic_bug(self):
        """
        For some reason, if one justifies the text in a widget, pyside2-uic
        generates code that doesn't work on Linux:
        self.ui.label_htp_help.setAlignment(Qt.AlignJustify|Qt.AlignTop)
        On Windows it just ignores the second argument, but on Linux it spits
        out an error:
        TypeError: 'PySide2.QtCore.Qt.AlignmentFlag' object cannot be
        interpreted as an integer
        The solution to this is to justify the text manually from the code, and
        not touch alignment settings at all in degigner.
        """
        self.ui.label_htp_help.setAlignment(Qt.AlignJustify)

    def _resize_window(self):
        if os.name == "nt":
            self.resize(700, 540)
        else:
            self.resize(730, 560)

    def _nop(self, x, y):
        pass

    def _fleet_creator_start(self):
        self._fleet_creator.start()
        self._fleet_creator_refresh()
        self.ui.stackedWidget.setCurrentIndex(1)

    def _htp_show(self):
        self.ui.stackedWidget.setCurrentIndex(3)

    def _return_to_main(self):
        self.ui.stackedWidget.setCurrentIndex(0)

    def _fleet_creator_left_click(self, x: str, y: int):
        if self._fleet_creator.contains_not_selected_ship(x, y):
            self._fleet_creator.select_ship(x, y)
        else:
            self._fleet_creator.set_ship_position(x, y)
        self._fleet_creator_refresh()

    def _fleet_creator_rand(self):
        self._fleet_creator.random_fleet()
        self._fleet_creator_refresh()

    def _fleet_creator_rot(self):
        self._fleet_creator.change_ship_rotation()
        self._fleet_creator_refresh()

    def _fleet_creator_done(self):
        board, fleet = self._fleet_creator.get_setup()
        self._game.start_game(board, fleet)
        self._game_refresh()
        self.ui.game_plain_text_edit_log.clear()
        self.ui.stackedWidget.setCurrentIndex(2)

    def _fleet_creator_refresh(self):
        board = self._fleet_creator.get_board_display()
        ship = self._fleet_creator.get_selected_ship()
        self._fleet_creator_board.update_board(board, ship)

    def _game_left_click(self, x: str, y: int):
        if self._game.won():
            self.ui.stackedWidget.setCurrentIndex(0)
        if self._game.players_turn():
            self._game.discover_field(x, y)
        else:
            self._game.enemy_move()
        self._game_refresh()

    def _game_right_click(self, x: str, y: int):
        status = self._game.get_enemy_board_display().get_field_status(x, y)
        if status != FieldStatus.MISS:
            self._game.mark_field(x, y)
        else:
            self._game.unmark_field(x, y)
        self._game_refresh()

    def _game_refresh(self):
        player_board = self._game.get_player_board_display()
        enemy_board = self._game.get_enemy_board_display()
        self._game_player_board.update_board(player_board, None)
        self._game_enemy_board.update_board(enemy_board, None)
        player_fleet = self._game.get_player_fleet_display()
        enemy_fleet = self._game.get_enemy_fleet_display()
        self._game_player_fleet.update_fleet_display(player_fleet)
        self._game_enemy_fleet.update_fleet_display(enemy_fleet)
        messages = self._game.get_display_messages()
        for message in messages:
            self.ui.game_plain_text_edit_log.insertPlainText(message)
        scrollbar = self.ui.game_plain_text_edit_log.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum() - 2)


def main(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument("--no-ui", required=False,
                        action="store_true",
                        help="launches the game in console")
    args = parser.parse_args(argv[1:])
    if args.no_ui:
        battleship = BattleshipCMD()
        battleship.start()
    else:
        app = QApplication(argv)
        battleship_window = BattleshipWindow()
        battleship_window.show()
        return app.exec_()


if __name__ == "__main__":
    main(sys.argv)
