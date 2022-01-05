import argparse
import sys
from enum import Enum

from PySide2.QtWidgets import QApplication

from game import cls, Game
from gui import BattleshipWindow


def choose(options_range):
    while True:
        try:
            choice = int(input("Choose an option: "))
            if 1 <= choice <= options_range:
                return choice
            else:
                print("Invalid option.")
        except ValueError:
            print("Invalid option.")


class BattleshipState(Enum):
    MAIN_MENU = 0,
    GAME = 1,
    HOW_TO_PLAY = 2


class Battleship:
    """
    Main application class
    """

    def __init__(self, window=None):
        """
        Initializes the menu and starts it
        """
        self._ui = None
        if window is not None:
            self._window: BattleshipWindow = window
            self._ui = self._window.ui
            self._ui.stackedWidget.setCurrentIndex(0)
        self._quit = False
        self._battleship_state = BattleshipState.MAIN_MENU
        if self._ui is not None:
            self._menu_ui_setup()

    def start(self):
        """
        Begins the main loop in the console version
        """
        while not self._quit and self._ui is None:
            if self._battleship_state == BattleshipState.MAIN_MENU:
                self._main_menu()
            elif self._battleship_state == BattleshipState.GAME:
                self._start_game()
            else:
                self._how_to_play()

    def _main_menu(self):
        """
        Displays the main menu
        """
        if self._ui is not None:
            self._ui.stackedWidget.setCurrentIndex(0)
            return
        main_menu = "Welcome to Battleship!\n" \
                    "1. Play the game\n" \
                    "2. How to play\n" \
                    "3. Exit\n" \
                    "\n"
        cls()
        print(main_menu)
        choice = choose(3)
        if choice == 1:
            self._battleship_state = BattleshipState.GAME
        elif choice == 2:
            self._battleship_state = BattleshipState.HOW_TO_PLAY
        else:
            self._quit = True

    def _start_game(self):
        """
        Starts the game, ends when the game ends
        """
        game = Game(self._ui)
        play = game.setup_player_board()
        if self._ui is None:
            if play:
                game.start_game()
            self._battleship_state = BattleshipState.MAIN_MENU

    def _basic_help(self):
        """
        Returns the basic help string, making it accessible to the UI as well
        as the console version
        """
        help_content = "How to play:\n" \
                       "The objective of this game is to destroy your " \
                       "opponent's fleet. You and your opponent shoot at " \
                       "chosen fields on the board, and get information " \
                       "whether you've hit or sunk you enemy's ship. If " \
                       "there was a hit, the player gets another move, if " \
                       "there isn't, the enemy gets to move.\n"
        return help_content

    def _how_to_play(self):
        """
        Shows help
        """
        if self._ui is not None:
            self._ui.stackedWidget.setCurrentIndex(3)
            return
        help_content = self._basic_help()
        controls = "In the console version, you perform moves by typing" \
                   "commands. You start a game with an automatically " \
                   "generated fleet that you can move around with commands\n" \
                   "sel <x> <y>, mv <x> <y> and rot\n" \
                   "sel selects a ship located at the specified " \
                   "coordinates, mv moves it to a new location, and rot " \
                   "rotates it. If you want to generate a completely new " \
                   "fleet, you can use\n" \
                   "rand\n" \
                   "When you're satisfied with the placements, you type\n" \
                   "done\n"
        game = "During the game, you can either shoot at your enemy's fleet" \
               "or mark fields as empty. You do that by using commands\n" \
               "st <x> <y>, mk <x> <y> and unmk <x> <y>\n" \
               "The first one shoots at the specified field, the second one" \
               "marks the field as empty, and the third one removes the" \
               "marker\n"
        common = "During the game, typing\n" \
                 "quit\n" \
                 "returns to the main menu. If you need help with the " \
                 "commands, you can use the\n" \
                 "help\n" \
                 "command."
        cls()
        print(help_content)
        print(controls)
        print(game)
        print(common)
        input()
        self._battleship_state = BattleshipState.MAIN_MENU

    def _menu_ui_setup(self):
        self._ui.button_play.clicked.connect(self._start_game)
        self._ui.button_htp.clicked.connect(self._how_to_play)
        self._ui.button_quit_game.clicked.connect(self._quit_game)
        self._ui.htp_content.setText(self._basic_help())
        self._ui.button_main_menu.clicked.connect(self._main_menu)

    def _quit_game(self):
        sys.exit(0)


def main(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument("--no-ui", required=False,
                        action="store_true",
                        help="launches the game in console")
    args = parser.parse_args(argv[1:])
    if args.no_ui:
        battleship = Battleship()
        battleship.start()
    else:
        app = QApplication()
        ui = BattleshipWindow()
        battleship = Battleship(ui)
        ui.show()
        battleship.start()
        return app.exec_()


if __name__ == "__main__":
    main(sys.argv)
