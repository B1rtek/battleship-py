# Battleship

Battleship game written in Python, with a GUI made in Qt5.

## Requirements:

* Python 3.9 or newer
* Packages: `PySide2`

## Usage

To launch the game, just execute the main file:

```shell
$ python3 battleship.py
```

The game will launch then in the GUI mode. If you prefer to play in terminal, you can add a flag:

```shell
$ python3 battleship.py --no-ui
```

and the game will launch in the terminal. Terminal version has not-so-great controls, so I'd recommend playing the
normal version. If you insist to play in terminal, make sure it's at least 30 lines tall or some content might not fit
on the screen. In game, you can always type `help` to get help about how to preform moves in the game or how to set
up your fleet.

## Other
In the `random_tests` directory there are some tests that study the behaviour of two "AI"s that you can play against in
game. There is a test showing how many moves the AI needs to win, which AI wins when they both play against each other,
where the ships are being placed most often while generating the board, and where each individual ship is getting
placed. All tests have charts generated from the data gathered, some in Excel, other ones generated with `matplotlib`
and `seaborn`, both of which are required to run these tests if you want to do it yourself.