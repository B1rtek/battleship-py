import argparse
import sys
from enum import Enum

from game import cls, Game
from ui_battleship import Ui_MainWindow


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

    def __init__(self, ui=None):
        """
        Initializes the menu and starts it
        """
        self._ui = ui
        self._quit = False
        self._battleship_state = BattleshipState.MAIN_MENU

    def start(self):
        """
        Begins the main loop in the console version
        """
        while not self._quit:
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
            pass
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
        game = Game()
        play = game.setup_player_board()
        if play:
            game.start_game()
        self._battleship_state = BattleshipState.MAIN_MENU

    def _how_to_play(self):
        """
        Shows help
        """
        if self._ui is not None:
            pass
            return
        help_content = "How to play:\n" \
                       "The objective of this game is to destroy your " \
                       "opponent's fleet. You and your opponents shoot at " \
                       "chosen fields on the board, and get information " \
                       "whether you've hit or sunk you enemy's ship. If " \
                       "there was a hit, the player gets another move, if " \
                       "there isn't, the enemy gets to move.\n"
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


def main(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument("--no-ui", required=False,
                        action="store_true",
                        help="launches the game in console")
    args = parser.parse_args(argv[1:])
    if args.no_ui:
        battleship = Battleship()
    else:
        ui = Ui_MainWindow()
        battleship = Battleship(ui)
    battleship.start()


if __name__ == "__main__":
    main(sys.argv)
