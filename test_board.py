import pytest

from board import Field, FieldStatus, game_to_array_coords, \
    InvalidGameCoordinatesError, Board, get_all_fields_coordinates, GameBoard
from fleet import Ship, Fleet


def test_field_create():
    field = Field()
    assert field.status() == FieldStatus.NOTHING


def test_field_set_status():
    field = Field()
    assert field.status() == FieldStatus.NOTHING
    field.set_status(FieldStatus.MISS)
    assert field.status() == FieldStatus.MISS


def test_field_str_nothing():
    field = Field()
    assert str(field) == ' '


def test_field_str_miss():
    field = Field()
    field.set_status(FieldStatus.MISS)
    assert str(field) == '.'


def test_field_str_ship():
    field = Field()
    field.set_status(FieldStatus.SHIP)
    assert str(field) == '█'


def test_field_str_sunk():
    field = Field()
    field.set_status(FieldStatus.SUNK)
    assert str(field) == '▒'


def test_field_str_selected():
    field = Field()
    field.set_status(FieldStatus.SELECTED)
    assert str(field) == '#'


def test_game_to_array_coords_typical():
    assert game_to_array_coords('a', 1) == (0, 0)


def test_game_to_array_coords_edge_case():
    assert game_to_array_coords('j', 10) == (9, 9)


def test_game_to_array_coords_x_too_low():
    with pytest.raises(InvalidGameCoordinatesError):
        game_to_array_coords('`', 10)


def test_game_to_array_coords_x_too_high():
    with pytest.raises(InvalidGameCoordinatesError):
        game_to_array_coords('k', 10)


def test_game_to_array_coords_y_too_low():
    with pytest.raises(InvalidGameCoordinatesError):
        game_to_array_coords('g', 0)


def test_game_to_array_coords_y_too_high():
    with pytest.raises(InvalidGameCoordinatesError):
        game_to_array_coords('g', 11)


def test_get_all_fields_coordinates():
    all_fields = get_all_fields_coordinates()
    assert all_fields == [('a', 1), ('b', 1), ('c', 1), ('d', 1), ('e', 1),
                          ('f', 1), ('g', 1), ('h', 1), ('i', 1), ('j', 1),
                          ('a', 2), ('b', 2), ('c', 2), ('d', 2), ('e', 2),
                          ('f', 2), ('g', 2), ('h', 2), ('i', 2), ('j', 2),
                          ('a', 3), ('b', 3), ('c', 3), ('d', 3), ('e', 3),
                          ('f', 3), ('g', 3), ('h', 3), ('i', 3), ('j', 3),
                          ('a', 4), ('b', 4), ('c', 4), ('d', 4), ('e', 4),
                          ('f', 4), ('g', 4), ('h', 4), ('i', 4), ('j', 4),
                          ('a', 5), ('b', 5), ('c', 5), ('d', 5), ('e', 5),
                          ('f', 5), ('g', 5), ('h', 5), ('i', 5), ('j', 5),
                          ('a', 6), ('b', 6), ('c', 6), ('d', 6), ('e', 6),
                          ('f', 6), ('g', 6), ('h', 6), ('i', 6), ('j', 6),
                          ('a', 7), ('b', 7), ('c', 7), ('d', 7), ('e', 7),
                          ('f', 7), ('g', 7), ('h', 7), ('i', 7), ('j', 7),
                          ('a', 8), ('b', 8), ('c', 8), ('d', 8), ('e', 8),
                          ('f', 8), ('g', 8), ('h', 8), ('i', 8), ('j', 8),
                          ('a', 9), ('b', 9), ('c', 9), ('d', 9), ('e', 9),
                          ('f', 9), ('g', 9), ('h', 9), ('i', 9), ('j', 9),
                          ('a', 10), ('b', 10), ('c', 10), ('d', 10),
                          ('e', 10), ('f', 10), ('g', 10), ('h', 10),
                          ('i', 10), ('j', 10)]


def test_board_create():
    board = Board()
    assert board.get_field_status('j', 10) == FieldStatus.NOTHING


def test_board_set_field_status():
    board = Board()
    board.set_field_status('a', 1, FieldStatus.SHIP)
    assert board.get_field_status('a', 1) == FieldStatus.SHIP


def test_board_str():
    board = Board()
    board.set_field_status('a', 1, FieldStatus.SHIP)
    board.set_field_status('a', 10, FieldStatus.MISS)
    board.set_field_status('j', 1, FieldStatus.SUNK)
    board.set_field_status('j', 10, FieldStatus.SELECTED)
    assert str(board) == "   abcdefghij\n" \
                         "\n" \
                         " 1 █        ▒\n" \
                         " 2           \n" \
                         " 3           \n" \
                         " 4           \n" \
                         " 5           \n" \
                         " 6           \n" \
                         " 7           \n" \
                         " 8           \n" \
                         " 9           \n" \
                         "10 .        #\n"


def test_board_clear_board():
    board = Board()
    board.set_field_status('b', 5, FieldStatus.SUNK)
    board.set_field_status('a', 10, FieldStatus.SELECTED)
    assert board.get_field_status('b', 5) == FieldStatus.SUNK
    assert board.get_field_status('a', 10) == FieldStatus.SELECTED
    board.clear_board()
    assert board.get_field_status('b', 5) == FieldStatus.NOTHING
    assert board.get_field_status('a', 10) == FieldStatus.NOTHING


def test_board_place_ship():
    board = Board()
    ship = Ship(('c', 4), 4, True)
    ship_segment_poss = [x.position() for x in ship.segments()]
    for x, y in ship_segment_poss:
        assert board.get_field_status(x, y) == FieldStatus.NOTHING
    board.place_ship(ship)
    for x, y in ship_segment_poss:
        assert board.get_field_status(x, y) == FieldStatus.SHIP


def test_board_place_fleet():
    board = Board()
    fleet = Fleet()
    fleet.create_random()
    ships = fleet.ships()
    ship_segment_poss = []
    for ship in ships:
        segments = ship.segments()
        for segment in segments:
            ship_segment_poss.append(segment.position())
    for x, y in get_all_fields_coordinates():
        assert board.get_field_status(x, y) == FieldStatus.NOTHING
    board.place_fleet(fleet)
    for x, y in get_all_fields_coordinates():
        if (x, y) in ship_segment_poss:
            assert board.get_field_status(x, y) == FieldStatus.SHIP
        else:
            assert board.get_field_status(x, y) == FieldStatus.NOTHING


def test_board_mark_sunken_ship():
    board = Board()
    ship = Ship(('d', 7), 4, False)
    ship_segment_poss = [x.position() for x in ship.segments()]
    for x, y in ship_segment_poss:
        assert board.get_field_status(x, y) == FieldStatus.NOTHING
    board.mark_sunken_ship(ship)
    for x, y in ship_segment_poss:
        assert board.get_field_status(x, y) == FieldStatus.SUNK


def test_gameboard_create():
    board = Board()
    fleet = Fleet()
    fleet.create_random()
    ships = fleet.ships()
    ship_segment_poss = []
    for ship in ships:
        segments = ship.segments()
        for segment in segments:
            ship_segment_poss.append(segment.position())
    board.place_fleet(fleet)
    gboard = GameBoard(board)
    visible_board = gboard.get_display_board(display_as_enemy=True)
    for x, y in get_all_fields_coordinates():
        assert visible_board.get_field_status(x, y) == FieldStatus.NOTHING
    data_board = gboard.get_display_board()
    for x, y in get_all_fields_coordinates():
        if (x, y) in ship_segment_poss:
            assert data_board.get_field_status(x, y) == FieldStatus.SHIP
        else:
            assert data_board.get_field_status(x, y) == FieldStatus.NOTHING


def test_gameboard_discover_field_miss():
    board = Board()
    gboard = GameBoard(board)
    hit = gboard.discover_field('b', 1)
    assert not hit
    data_board = gboard.get_display_board()
    assert data_board.get_field_status('b', 1) == FieldStatus.MISS
    visible_board = gboard.get_display_board(display_as_enemy=True)
    assert visible_board.get_field_status('b', 1) == FieldStatus.MISS


def test_gameboard_discover_field_hit():
    board = Board()
    fleet = Fleet()
    fleet.create_random()
    board.place_fleet(fleet)
    guaranteed_hit_pos = fleet.ships()[0].segments()[0].position()
    gboard = GameBoard(board)
    x, y = guaranteed_hit_pos
    hit = gboard.discover_field(x, y)
    assert hit
    data_board = gboard.get_display_board()
    assert data_board.get_field_status(x, y) == FieldStatus.SUNK
    visible_board = gboard.get_display_board(display_as_enemy=True)
    assert visible_board.get_field_status(x, y) == FieldStatus.SHIP


def test_gameboard_discover_field_sunk():
    board = Board()
    fleet = Fleet()
    fleet.create_random()
    board.place_fleet(fleet)
    guaranteed_sink_pos = fleet.ships()[9].segments()[0].position()
    gboard = GameBoard(board)
    x, y = guaranteed_sink_pos
    hit = gboard.discover_field(x, y)
    assert hit
    data_board = gboard.get_display_board()
    assert data_board.get_field_status(x, y) == FieldStatus.SUNK
    visible_board = gboard.get_display_board(display_as_enemy=True)
    assert visible_board.get_field_status(x, y) == FieldStatus.SUNK


def test_gameboard_mark_as_empty():
    board = Board()
    gboard = GameBoard(board)
    marked = gboard.mark_as_empty('a', 1)
    assert marked
    data_board = gboard.get_display_board()
    assert data_board.get_field_status('a', 1) == FieldStatus.NOTHING
    visible_board = gboard.get_display_board(display_as_enemy=True)
    assert visible_board.get_field_status('a', 1) == FieldStatus.MISS


def test_gameboard_mark_as_empty_fail():
    board = Board()
    gboard = GameBoard(board)
    marked = gboard.mark_as_empty('a', 1)
    assert marked
    marked_again = gboard.mark_as_empty('a', 1)
    assert not marked_again
    data_board = gboard.get_display_board()
    assert data_board.get_field_status('a', 1) == FieldStatus.NOTHING
    visible_board = gboard.get_display_board(display_as_enemy=True)
    assert visible_board.get_field_status('a', 1) == FieldStatus.MISS



