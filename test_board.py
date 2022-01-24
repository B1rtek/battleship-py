import pytest

from board import Field, FieldStatus, game_to_array_coords, \
    InvalidGameCoordinatesError, Board, GameBoard, \
    return_all_field_coordinates
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
    all_fields = return_all_field_coordinates()
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
    for x, y in return_all_field_coordinates():
        assert board.get_field_status(x, y) == FieldStatus.NOTHING
    board.place_fleet(fleet)
    for x, y in return_all_field_coordinates():
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
    board_seen_by_enemy = gboard.get_display_board(display_as_enemy=True)
    for x, y in return_all_field_coordinates():
        assert board_seen_by_enemy. \
                   get_field_status(x, y) == FieldStatus.NOTHING
    board_seen_by_player = gboard.get_display_board()
    for x, y in return_all_field_coordinates():
        if (x, y) in ship_segment_poss:
            assert board_seen_by_player. \
                       get_field_status(x, y) == FieldStatus.SHIP
        else:
            assert board_seen_by_player. \
                       get_field_status(x, y) == FieldStatus.NOTHING


def test_gameboard_discover_field_miss():
    board = Board()
    gboard = GameBoard(board)
    hit = gboard.discover_field('b', 1)
    assert not hit
    board_seen_by_player = gboard.get_display_board()
    assert board_seen_by_player.get_field_status('b', 1) == FieldStatus.MISS
    board_seen_by_enemy = gboard.get_display_board(display_as_enemy=True)
    assert board_seen_by_enemy.get_field_status('b', 1) == FieldStatus.MISS


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
    board_seen_by_player = gboard.get_display_board()
    assert board_seen_by_player.get_field_status(x, y) == FieldStatus.SUNK
    board_seen_by_enemy = gboard.get_display_board(display_as_enemy=True)
    assert board_seen_by_enemy.get_field_status(x, y) == FieldStatus.SHIP


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
    board_seen_by_player = gboard.get_display_board()
    assert board_seen_by_player.get_field_status(x, y) == FieldStatus.SUNK
    board_seen_by_enemy = gboard.get_display_board(display_as_enemy=True)
    assert board_seen_by_enemy.get_field_status(x, y) == FieldStatus.SHIP
    # This is intended behaviour. Only after confirming that the ship was sunk
    # the sink_ship() method is called and the ship gets marked as sunk for
    # the enemy, this suggests that the hit ship isn't sunk yet and the enemy
    # should search for the other parts of it
    sunk = fleet.hit(x, y)
    assert sunk
    ship_to_sink = fleet.find_ship(x, y)
    gboard.sink_ship(ship_to_sink)
    board_seen_by_player = gboard.get_display_board()
    assert board_seen_by_player.get_field_status(x, y) == FieldStatus.SUNK
    board_seen_by_enemy = gboard.get_display_board(display_as_enemy=True)
    assert board_seen_by_enemy.get_field_status(x, y) == FieldStatus.SUNK


def test_gameboard_mark_as_empty():
    board = Board()
    gboard = GameBoard(board)
    marked = gboard.mark_as_empty('a', 1)
    assert marked
    board_seen_by_player = gboard.get_display_board()
    assert board_seen_by_player.get_field_status('a', 1) == FieldStatus.MISS
    board_seen_by_enemy = gboard.get_display_board(display_as_enemy=True)
    assert board_seen_by_enemy.get_field_status('a', 1) == FieldStatus.MISS
    # Both players can see which fields have been marked by their enemy. It
    # gives the player the idea how much moves he can survive, and the markers
    # placed by the player prevent the player from shooting at these fields.


def test_gameboard_mark_as_empty_fail_field_marked():
    board = Board()
    gboard = GameBoard(board)
    marked = gboard.mark_as_empty('a', 1)
    assert marked
    marked_again = gboard.mark_as_empty('a', 1)
    assert not marked_again
    board_seen_by_player = gboard.get_display_board()
    assert board_seen_by_player.get_field_status('a', 1) == FieldStatus.MISS
    board_seen_by_enemy = gboard.get_display_board(display_as_enemy=True)
    assert board_seen_by_enemy.get_field_status('a', 1) == FieldStatus.MISS


def test_gameboard_mark_as_empty_fail_ship_on_field():
    board = Board()
    fleet = Fleet()
    fleet.create_random()
    board.place_fleet(fleet)
    guaranteed_hit_pos = fleet.ships()[0].segments()[0].position()
    gboard = GameBoard(board)
    x, y = guaranteed_hit_pos
    hit = gboard.discover_field(x, y)
    assert hit
    marked = gboard.mark_as_empty(x, y)
    assert not marked
    board_seen_by_player = gboard.get_display_board()
    assert board_seen_by_player.get_field_status(x, y) == FieldStatus.SUNK
    board_seen_by_enemy = gboard.get_display_board(display_as_enemy=True)
    assert board_seen_by_enemy.get_field_status(x, y) == FieldStatus.SHIP


def test_gameboard_unmark_as_empty():
    board = Board()
    gboard = GameBoard(board)
    marked = gboard.mark_as_empty('a', 1)
    assert marked
    unmarked = gboard.unmark_as_empty('a', 1)
    assert unmarked
    board_seen_by_player = gboard.get_display_board()
    assert board_seen_by_player.get_field_status('a', 1) == FieldStatus.NOTHING
    board_seen_by_enemy = gboard.get_display_board(display_as_enemy=True)
    assert board_seen_by_enemy.get_field_status('a', 1) == FieldStatus.NOTHING


def test_gameboard_unmark_as_empty_fail_not_marked():
    board = Board()
    gboard = GameBoard(board)
    unmarked = gboard.unmark_as_empty('a', 1)
    assert not unmarked
    board_seen_by_player = gboard.get_display_board()
    assert board_seen_by_player.get_field_status('a', 1) == FieldStatus.NOTHING
    board_seen_by_enemy = gboard.get_display_board(display_as_enemy=True)
    assert board_seen_by_enemy.get_field_status('a', 1) == FieldStatus.NOTHING


def test_gameboard_unmark_as_empty_fail_field_not_empty():
    board = Board()
    fleet = Fleet()
    fleet.create_random()
    board.place_fleet(fleet)
    guaranteed_hit_pos = fleet.ships()[0].segments()[0].position()
    gboard = GameBoard(board)
    x, y = guaranteed_hit_pos
    hit = gboard.discover_field(x, y)
    assert hit
    unmarked = gboard.unmark_as_empty(x, y)
    assert not unmarked
    board_seen_by_player = gboard.get_display_board()
    assert board_seen_by_player.get_field_status(x, y) == FieldStatus.SUNK
    board_seen_by_enemy = gboard.get_display_board(display_as_enemy=True)
    assert board_seen_by_enemy.get_field_status(x, y) == FieldStatus.SHIP


def test_gameboard_sink_ship():
    board = Board()
    fleet = Fleet()
    fleet.create_random()
    board.place_fleet(fleet)
    ship_segments_to_sink = [x.position() for x in fleet.ships()[2].segments()]
    gboard = GameBoard(board)
    board_seen_by_player = gboard.get_display_board()
    board_seen_by_enemy = gboard.get_display_board(display_as_enemy=True)
    for x, y in ship_segments_to_sink:
        assert board_seen_by_player. \
                   get_field_status(x, y) == FieldStatus.SHIP
        assert board_seen_by_enemy. \
                   get_field_status(x, y) == FieldStatus.NOTHING
    for x, y in ship_segments_to_sink:
        gboard.discover_field(x, y)
    board_seen_by_player = gboard.get_display_board()
    board_seen_by_enemy = gboard.get_display_board(display_as_enemy=True)
    for x, y in ship_segments_to_sink:
        assert board_seen_by_player. \
                   get_field_status(x, y) == FieldStatus.SUNK
        assert board_seen_by_enemy. \
                   get_field_status(x, y) == FieldStatus.SHIP
    x, y = ship_segments_to_sink[0]
    ship_to_sink = fleet.find_ship(x, y)
    gboard.sink_ship(ship_to_sink)
    board_seen_by_player = gboard.get_display_board()
    board_seen_by_enemy = gboard.get_display_board(display_as_enemy=True)
    for x, y in ship_segments_to_sink:
        assert board_seen_by_player. \
                   get_field_status(x, y) == FieldStatus.SUNK
        assert board_seen_by_enemy. \
                   get_field_status(x, y) == FieldStatus.SUNK


def test_gameboard_field_undiscovered():
    board = Board()
    fleet = Fleet()
    fleet.create_random()
    board.place_fleet(fleet)
    gboard = GameBoard(board)
    assert gboard.field_undiscovered('a', 1)


def test_gameboard_field_undiscovered_discovered():
    board = Board()
    fleet = Fleet()
    fleet.create_random()
    board.place_fleet(fleet)
    gboard = GameBoard(board)
    gboard.discover_field('a', 1)
    assert not gboard.field_undiscovered('a', 1)


def test_mark_misses_around(monkeypatch):
    def rigged_fleet(self):
        self._ships.clear()
        ships = []
        ships.append(Ship(('a', 1), 4, False))
        ships.append(Ship(('a', 3), 3, False))
        ships.append(Ship(('a', 5), 3, False))
        ships.append(Ship(('a', 7), 2, False))
        ships.append(Ship(('a', 9), 2, False))
        ships.append(Ship(('f', 5), 2, False))
        ships.append(Ship(('f', 1), 1, False))
        ships.append(Ship(('h', 1), 1, False))
        ships.append(Ship(('j', 1), 1, False))
        ships.append(Ship(('j', 10), 1, False))
        self._ships = ships

    monkeypatch.setattr("fleet.Fleet.create_random", rigged_fleet)

    board = Board()
    fleet = Fleet()
    fleet.create_random()
    board.place_fleet(fleet)
    gboard = GameBoard(board)
    ship_to_sink = fleet.find_ship('f', 5)
    segments = [x.position() for x in ship_to_sink.segments()]
    fields_around = [('e', 4), ('e', 5), ('e', 6), ('f', 4), ('f', 6),
                     ('g', 4), ('g', 6), ('h', 4), ('h', 5), ('h', 6), ]
    gboard.sink_ship(ship_to_sink)
    board_seen_by_player = gboard.get_display_board()
    board_seen_by_enemy = gboard.get_display_board(display_as_enemy=True)
    for x, y in segments:
        assert board_seen_by_player. \
            get_field_status(x, y) == FieldStatus.SUNK
        assert board_seen_by_enemy. \
            get_field_status(x, y) == FieldStatus.SUNK
    for x, y in fields_around:
        assert board_seen_by_player. \
            get_field_status(x, y) == FieldStatus.NOTHING
        assert board_seen_by_enemy. \
            get_field_status(x, y) == FieldStatus.NOTHING
    gboard.mark_misses_around(ship_to_sink)
    for x, y in segments:
        assert board_seen_by_player. \
            get_field_status(x, y) == FieldStatus.SUNK
        assert board_seen_by_enemy. \
            get_field_status(x, y) == FieldStatus.SUNK
    for x, y in fields_around:
        assert board_seen_by_player. \
            get_field_status(x, y) == FieldStatus.NOTHING
        assert board_seen_by_enemy. \
            get_field_status(x, y) == FieldStatus.MISS
    # This function is used to automatically mark fields around when the ship
    # sinks, and these markers cannot be seen by the player as they aren't
    # placed by the enemy, but show up on their board automatically
