import argparse
import os
import sys
from enum import Enum
from typing import List

from PySide2.QtCore import Qt
from PySide2.QtWidgets import QApplication, QMainWindow

from board import FieldStatus
from fleet_creator import FleetCreator, FCMessage
from game import Game, GameMessage
from gui import UIBoard, load_icons, UIFleet
from settings import Settings, Setting
from ui_battleship import Ui_Battleship


class AppState(Enum):
    MAIN_MENU = 0,
    SETUP = 1,
    GAME = 2,
    HOW_TO_PLAY = 3,
    SETTINGS = 4


class Command(Enum):
    NOP = 0,
    MAIN_START_SETUP = 1,
    MAIN_SETTINGS = 2,
    MAIN_START_HTP = 3,
    MAIN_EXIT = 4,
    EXIT_TO_MAIN = 5,
    CREATOR_SHIP_SELECT = 6,
    CREATOR_SHIP_MOVE = 7,
    CREATOR_SHIP_ROTATE = 8,
    CREATOR_FLEET_RAND = 9,
    CREATOR_DONE = 10,
    CREATOR_HELP = 11,
    GAME_SHOOT = 12,
    GAME_MARK_FIELD = 13,
    GAME_UNMARK_FIELD = 14,
    GAME_HELP = 15,
    SETTINGS_MMA = 16,
    SETTINGS_HARD_ENEMY = 17


def cls():
    """
    Clears the console
    """
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")


def format_fleet_creator_messages(messages: List[FCMessage]) -> str:
    """
    Formats the messages from FleetCreator, creating a string with all of them
    :param messages: messages from FleetCreator
    :type messages: list
    :return: string with all messages formatted
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

    messages_dict = {
        FCMessage.SHIP_SELECTED: "A ship has been selected",
        FCMessage.SHIP_MOVE_FAIL: "The selected location is invalid",
        FCMessage.SHIP_ROTATION_FAIL: "You can't rotate this ship",
        FCMessage.SETUP_HELP: help_content
    }

    messages_list = [messages_dict[x] for x in messages]
    formatted_messages = '\n'.join(messages_list)
    return formatted_messages


def format_game_messages(messages: List[GameMessage],
                         extra_newline: bool = False) -> str:
    """
    Formats the messages from Game, creating a string with all of them
    :param messages: messages from Game
    :type messages: list
    :return: string with all messages formatted
    """
    help_content = "Help:\n" \
                   "st <x> <y>: shoots at the specified field\n" \
                   "mk <x> <y>: marks the specified field on the " \
                   "enemy's board as empty\n" \
                   "unmk <x> <y>: unmarks the specified field\n" \
                   "quit: quits the game"

    messages_dict = {
        GameMessage.NOT_PLAYERS_TURN: "It's not your turn!",
        GameMessage.INVALID_COORDS: "Invalid field coordinates",
        GameMessage.ENEMY_SHIP_HIT: "You've hit an enemy ship!",
        GameMessage.ENEMY_SHIP_SUNK: "You've destroyed an enemy ship!",
        GameMessage.ENEMY_MISS: "Enemy has missed. It's your turn now.",
        GameMessage.ENEMY_WIN: "Enemy wins.",
        GameMessage.FIELD_MARK_FAIL: "The field you tried to mark has a "
                                     "discovered ship",
        GameMessage.FIELD_UNMARK_FAIL: "The field you tried to unmark isn't "
                                       "marked",
        GameMessage.GAME_HELP: help_content,
        GameMessage.PLAYER_SHIP_HIT: "Enemy has hit one of your ships!",
        GameMessage.PLAYER_SHIP_SUNK: "Enemy has destroyed one of your ships!",
        GameMessage.PLAYER_MISS: "You missed. Press to continue to the next "
                                 "enemy move",
        GameMessage.PLAYER_WIN: "You win!",
        GameMessage.FIELD_ALREADY_DISCOVERED: "This field has been already "
                                              "discovered",
        GameMessage.PLAYERS_TURN: "It's your turn."
    }

    messages_list = [messages_dict[x] for x in messages]
    formatted_messages = '\n'.join(messages_list)
    if extra_newline:
        formatted_messages += '\n'
    return formatted_messages


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
        self._settings = Settings()
        self._settings.load_settings()
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
        elif self._state == AppState.HOW_TO_PLAY:
            self._display_help()
        else:
            self._display_settings()

    def _display_main_menu(self):
        """
        Displays (prints out) the Main Menu
        """
        menu_content = "Welcome to Battleship!\n" \
                       "1. Play the game\n" \
                       "2. Settings\n" \
                       "3. How to play\n" \
                       "4. Exit\n" \
                       "\n"
        print(menu_content)

    def _display_fleet_creator(self):
        """
        Displays (prints out) the Fleet Creator
        """
        display_board = self._fleet_creator.get_board_display()
        print("Set up your fleet:")
        print(display_board)
        messages = self._fleet_creator.get_display_messages()
        print(format_fleet_creator_messages(messages))

    def _display_game(self):
        """
        Displays (prints out) the Game
        """
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
        print(format_game_messages(messages))

    def _display_help(self):
        """
        Displays (prints out) the Help screen
        """
        help_content = "How to play:\n" \
                       "The objective of this game is to destroy your " \
                       "opponent's fleet. You and your opponent shoot at " \
                       "chosen fields on the board, and get information " \
                       "whether you've hit or sunk you enemy's ship. If " \
                       "there was a hit, the player gets another move, if " \
                       "there isn't, the enemy gets to move.\n"
        print(help_content)

    def _display_settings(self):
        """
        Displays the settings page
        """
        settings_list = [
            "1. Mark fields around sunken ships:",
            "2. Harder enemy: "
        ]
        settings = self._settings.get_settings()
        states = ["Yes" if x else "No" for x in settings.values()]
        for setting, state in zip(settings_list, states):
            print(f"{setting} {state}")

    def _player_input(self) -> tuple[Command, str, int]:
        """
        Handles user input and interprets it, creating a command tuple
        :return: tuple containing a command and its arguments
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
        elif self._state == AppState.HOW_TO_PLAY:
            return Command.EXIT_TO_MAIN, "", 0
        else:
            return self._player_input_settings(command_parts)

    def _player_input_main_menu(self, command_parts: list[str]) -> \
            tuple[Command, str, int]:
        """
        Interprets the Main Menu commands
        :param command_parts: sliced user input
        :type command_parts: tuple
        :return: formatted command
        """
        if len(command_parts) == 0:
            return Command.NOP, "", 0
        else:
            if command_parts[0].startswith('1'):
                return Command.MAIN_START_SETUP, "", 0
            elif command_parts[0].startswith('2'):
                return Command.MAIN_SETTINGS, "", 0
            elif command_parts[0].startswith('3'):
                return Command.MAIN_START_HTP, "", 0
            elif command_parts[0].startswith('4'):
                return Command.MAIN_EXIT, "", 0
            else:
                return Command.NOP, "", 0

    def _player_input_fleet_creator(self, command_parts: list[str]) -> \
            tuple[Command, str, int]:
        """
        Interprets the Fleet Creator commands
        :param command_parts: sliced user input
        :type command_parts: tuple
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
        Interprets the Game commands
        :param command_parts: sliced user input
        :type command_parts: tuple
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

    def _player_input_settings(self, command_parts: list[str]) -> \
            tuple[Command, str, int]:
        if len(command_parts) == 0:
            return Command.NOP, "", 0
        else:
            if command_parts[0].startswith('1'):
                return Command.SETTINGS_MMA, "", 0
            elif command_parts[0].startswith('2'):
                return Command.SETTINGS_HARD_ENEMY, "", 0
            else:
                return Command.EXIT_TO_MAIN, "", 0

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
        elif self._state == AppState.SETTINGS:
            self._execute_settings(command)

    def _execute_main_menu(self, command):
        """
        Executes Main Menu commands
        :param command: command as a Command class enum
        :type command: Command
        """
        if command == Command.MAIN_START_SETUP:
            self._fleet_creator.start()
            self._state = AppState.SETUP
        elif command == Command.MAIN_SETTINGS:
            self._state = AppState.SETTINGS
        elif command == Command.MAIN_START_HTP:
            self._state = AppState.HOW_TO_PLAY
        elif command == Command.MAIN_EXIT:
            self._quit = True

    def _execute_fleet_creator(self, command, x, y):
        """
        Executes Fleet Creator commands
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
        Executes Game commands
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

    def _execute_settings(self, command: Command):
        if command == Command.SETTINGS_MMA:
            setting_mma = self._settings.get_settings()[
                Setting.MARK_MISSES_AROUND]
            self._settings.set_mark_misses_around(not setting_mma)
        elif command == Command.SETTINGS_HARD_ENEMY:
            setting_hard_enemy = self._settings.get_settings()[
                Setting.HARD_ENEMY]
            self._settings.set_hard_enemy(not setting_hard_enemy)
        else:
            self._game.apply_settings(self._settings.get_settings())
            self._state = AppState.MAIN_MENU

    def start(self):
        """
        Begins the "fetch-execute" loop, which displays the current contents,
        fetches the command from the user, interprets it and executes it
        """
        while not self._quit:
            self._display()
            command, x, y = self._player_input()
            self._execute(command, x, y)
        self._settings.save_settings()


class BattleshipWindow(QMainWindow):
    """
    Class operating the game in the GUI version
    """

    def __init__(self, parent=None):
        """
        Initializes all elements of the game and all additional widgets created
        in code rather than in the designer like UIBoards and UIFleets
        :param parent: parent widget, in this case always None
        """
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
        self._settings = Settings()
        self._settings.load_settings()
        self._setup_boards()
        self._setup_fleet_displays()
        self._link_buttons()
        self._load_settings()
        self._resize_window()
        self._fix_pyside2_uic_bug()
        self.ui.stackedWidget.setCurrentIndex(0)

    def mousePressEvent(self, QMouseEvent):
        """
        Registers left mouse clicks on the window outside of buttons, used to
        advance the game to the next enemy move without the need for a player
        to click a dedicated button, it makes it easier to interact with the
        game
        :param QMouseEvent: QMouseEvent generated with the mouse click
        :type QMouseEvent: QMouseEvent
        """
        if self.ui.stackedWidget.currentIndex() == 2:  # in Game
            if not self._game.players_turn():
                self._game.enemy_move()
                self._game_refresh()
            if self._game.won():
                self.ui.stackedWidget.setCurrentIndex(0)

    def _setup_boards(self):
        """
        Creates the Game and Fleet Creator boards in the UI, initializes them,
        assigns actions to their buttons and places them in their target Grid
        Layouts
        """
        icons = load_icons()
        self._fleet_creator_board.set_icons(icons)
        self._game_player_board.set_icons(icons)
        self._game_enemy_board.set_icons(icons)
        self._fleet_creator_board.define_left_click_action(
            self._fleet_creator_left_click)
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
        """
        Creates the UIFleets in the UI, initializes them, assigns actions to
        their buttons (triggering the enemy moves if it's enemy move, just like
        the mousePressEvent does) and places them in their target Grid Layouts
        """
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
        Assigns functions to all UI buttons' clicked signals
        """
        self.ui.button_main_play.clicked.connect(self._fleet_creator_start)
        self.ui.button_main_htp.clicked.connect(self._htp_show)
        self.ui.button_main_settings.clicked.connect(self._settings_show)
        self.ui.button_main_quit.clicked.connect(self._quit)
        self.ui.button_setup_exit.clicked.connect(self._return_to_main)
        self.ui.button_setup_rand.clicked.connect(self._fleet_creator_rand)
        self.ui.button_setup_rot.clicked.connect(self._fleet_creator_rot)
        self.ui.button_setup_done.clicked.connect(self._fleet_creator_done)
        self.ui.button_game_main.clicked.connect(self._return_to_main)
        self.ui.button_htp_back.clicked.connect(self._return_to_main)
        self.ui.button_settings_back.clicked.connect(
            self._settings_save_and_back)
        self.ui.checkbox_settings_mma.stateChanged.connect(
            self._settings_toggle_mma)
        self.ui.checkbox_settings_hard_enemy.stateChanged.connect(
            self._settings_toggle_hard_enemy)

    def _load_settings(self):
        settings = self._settings.get_settings()
        self.ui.checkbox_settings_mma.setChecked(
            settings[Setting.MARK_MISSES_AROUND])
        self.ui.checkbox_settings_hard_enemy.setChecked(
            settings[Setting.HARD_ENEMY])
        self._game.apply_settings(self._settings.get_settings())

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
        not touch alignment settings at all in designer.
        """
        self.ui.label_htp_help.setAlignment(Qt.AlignJustify)

    def _resize_window(self):
        """
        Resizes the window to the smallest size in which the game screen looks
        good. The window can be resized afterwards, but the buttons which
        represent the boards might be a bit squished
        """
        if os.name == "nt":
            self.resize(700, 540)
        else:
            self.resize(730, 560)

    def _fleet_creator_start(self):
        """
        Starts the Fleet Creator, starting the setup stage of the game
        """
        self._fleet_creator.start()
        self._fleet_creator_refresh()
        self.ui.stackedWidget.setCurrentIndex(1)

    def _htp_show(self):
        """
        Shows the How To Play page
        """
        self.ui.stackedWidget.setCurrentIndex(3)

    def _return_to_main(self):
        """
        Returns to the Main Menu
        """
        self.ui.stackedWidget.setCurrentIndex(0)

    def _fleet_creator_left_click(self, x: str, y: int):
        """
        Performs the left click operations in the Fleet Creator, and refreshes
        the Fleet Creator board afterwards
        :param x: x argument of a command called by a button that this function
        was assigned to, in this case the letter of the row on the board
        :type x: str
        :param y: y argument of a command called by a button that this function
        was assigned to, in this case the number of the column on the board
        :type y: int
        """
        if self._fleet_creator.contains_not_selected_ship(x, y):
            self._fleet_creator.select_ship(x, y)
        else:
            self._fleet_creator.set_ship_position(x, y)
        self._fleet_creator_refresh()

    def _fleet_creator_rand(self):
        """
        Calls the function in the Fleet Creator which creates a new random
        fleet, and refreshes the Fleet Creator board afterwards
        """
        self._fleet_creator.random_fleet()
        self._fleet_creator_refresh()

    def _fleet_creator_rot(self):
        """
        Calls the function in the Fleet Creator which rotates the selected
        ship, and refreshes the Fleet Creator board afterwards
        """
        self._fleet_creator.change_ship_rotation()
        self._fleet_creator_refresh()

    def _fleet_creator_done(self):
        """
        Ends the setup stage of the game ans starts the Game itself, passing
        the created fleet from the Fleet Creator to the Game as the player's
        fleet
        """
        board, fleet = self._fleet_creator.get_setup()
        self._game.start_game(board, fleet)
        self.ui.game_plain_text_edit_log.clear()
        self._game_refresh()
        self.ui.stackedWidget.setCurrentIndex(2)

    def _fleet_creator_refresh(self):
        """
        Refreshes the Fleet Creator UIBoard after performing an action
        """
        board = self._fleet_creator.get_board_display()
        ship = self._fleet_creator.get_selected_ship()
        self._fleet_creator_board.update_board(board, ship)

    def _game_left_click(self, x: str, y: int):
        """
        Performs the left click operations in the Game, and refreshes all Game
        UI elements afterwards
        :param x: x argument of a command called by a button that this function
        was assigned to, in this case the letter of the row on the board
        :type x: str
        :param y: y argument of a command called by a button that this function
        was assigned to, in this case the number of the column on the board
        :type y: int
        """
        if self._game.won():
            self.ui.stackedWidget.setCurrentIndex(0)
        if self._game.players_turn():
            self._game.discover_field(x, y)
        else:
            self._game.enemy_move()
        self._game_refresh()

    def _game_right_click(self, x: str, y: int):
        """
        Performs the right click operations in the Game, and refreshes all Game
        UI elements afterwards
        :param x: x argument of a command called by a button that this function
        was assigned to, in this case the letter of the row on the board
        :type x: str
        :param y: y argument of a command called by a button that this function
        was assigned to, in this case the number of the column on the board
        :type y: int
        """
        status = self._game.get_enemy_board_display().get_field_status(x, y)
        if status != FieldStatus.MISS:
            self._game.mark_field(x, y)
        else:
            self._game.unmark_field(x, y)
        self._game_refresh()

    def _game_refresh(self):
        """
        Refreshes all Game UI elements after player or the enemy performs a
        move
        """
        player_board = self._game.get_player_board_display()
        enemy_board = self._game.get_enemy_board_display()
        self._game_player_board.update_board(player_board, None)
        self._game_enemy_board.update_board(enemy_board, None)
        player_fleet = self._game.get_player_fleet_display()
        enemy_fleet = self._game.get_enemy_fleet_display()
        self._game_player_fleet.update_fleet_display(player_fleet)
        self._game_enemy_fleet.update_fleet_display(enemy_fleet)
        messages = self._game.get_display_messages()
        formatted = format_game_messages(messages, extra_newline=True)
        self.ui.game_plain_text_edit_log.insertPlainText(formatted)
        scrollbar = self.ui.game_plain_text_edit_log.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum() - 2)

    def _settings_show(self):
        self.ui.stackedWidget.setCurrentIndex(4)

    def _settings_toggle_mma(self):
        new_state = self.ui.checkbox_settings_mma.isChecked()
        self._settings.set_mark_misses_around(new_state)

    def _settings_toggle_hard_enemy(self):
        new_state = self.ui.checkbox_settings_hard_enemy.isChecked()
        self._settings.set_hard_enemy(new_state)

    def _settings_save_and_back(self):
        self._game.apply_settings(self._settings.get_settings())
        self._return_to_main()

    def _quit(self):
        self._settings.save_settings()
        sys.exit(0)


def main(argv):
    """
    The main function, parses the command line arguments and starts the correct
    version of the game according to those arguments
    :param argv: command line arguments
    :type argv: list
    """
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
